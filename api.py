import os
import json
from io import BytesIO
from typing import List, Optional
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from docx import Document as DocxDocument
from PyPDF2 import PdfReader

from rag import CareerRAG
from rag2 import router as chat_router

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(title="Career Compass RAG API", version="1.0.0")
app.include_router(chat_router)
BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


class SimilarDoc(BaseModel):
    content: str
    score: float
    source: Optional[str] = None
    section: Optional[int] = None


class StructuredProfileRequest(BaseModel):
    degree: str = Field(..., examples=["B.Tech"])
    branch: str = Field(..., examples=["CSE"])
    experience: int = Field(..., ge=0, le=50, examples=[0])
    experience_type: str = Field(..., examples=["No experience"])
    skills: str = Field(..., examples=["Python, Machine Learning, SQL, Cloud"])
    interests: str = Field(..., examples=["AI/ML, Data Science, Infrastructure"])


class NaturalProfileRequest(BaseModel):
    description: str = Field(..., min_length=5)


class RecommendResponse(BaseModel):
    recommendation: str
    confidence: float
    similar: List[SimilarDoc]


class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=5)


class YouTubePlaylist(BaseModel):
    title: str
    url: str
    channel: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class PlaylistSuggestionRequest(BaseModel):
    recommendation: str = Field(..., min_length=5)
    max_results: int = Field(default=6, ge=1, le=20)


def _extract_resume_text(file: UploadFile) -> str:
    filename = (file.filename or "").strip()
    ext = os.path.splitext(filename.lower())[1]
    data = file.file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        if ext == ".pdf":
            reader = PdfReader(BytesIO(data))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n".join(pages).strip()
        elif ext == ".docx":
            doc = DocxDocument(BytesIO(data))
            text = "\n".join(p.text for p in doc.paragraphs).strip()
        elif ext == ".doc":
            raise HTTPException(
                status_code=400,
                detail="Legacy .doc is not supported. Please upload .pdf or .docx",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload .pdf or .docx",
            )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read resume: {exc}")

    if len(text) < 30:
        raise HTTPException(
            status_code=400,
            detail="Could not extract enough text from resume. Try another file.",
        )
    return text[:12000]


def _init_rag() -> CareerRAG:
    rag = CareerRAG()
    try:
        rag.load_vector_store()
    except Exception:
        rag.create_vector_store()
        rag.save_vector_store()
    return rag


def _set_rag_state(rag: Optional[CareerRAG], error: Optional[str]) -> None:
    app.state.rag = rag
    app.state.init_error = error


def _get_rag() -> CareerRAG:
    rag = getattr(app.state, "rag", None)
    if rag is not None:
        return rag

    # Lazy init fallback: if startup failed or did not complete, try once on demand.
    try:
        rag = _init_rag()
        _set_rag_state(rag, None)
        return rag
    except Exception as exc:
        error = str(exc)
        _set_rag_state(None, error)
        raise HTTPException(
            status_code=503,
            detail=f"RAG system not initialized: {error}",
        )
    return rag


def _similar_docs(rag: CareerRAG, query: str, top_k: int = 3) -> List[SimilarDoc]:
    docs_and_scores = rag.retrieve_similar_documents(query, top_k=top_k)
    result: List[SimilarDoc] = []
    for doc, score in docs_and_scores:
        result.append(
            SimilarDoc(
                content=doc.page_content,
                score=float(score),
                source=doc.metadata.get("source"),
                section=doc.metadata.get("section"),
            )
        )
    return result


def _build_youtube_queries_from_recommendation(text: str) -> List[str]:
    lower = text.lower()
    query_map = [
        (["python"], "python programming full course playlist"),
        (["data structures", "algorithms", "dsa"], "data structures and algorithms playlist"),
        (["machine learning", "ml"], "machine learning roadmap playlist"),
        (["deep learning", "neural network"], "deep learning playlist"),
        (["data science", "data scientist"], "data science complete playlist"),
        (["sql", "database"], "sql and database playlist"),
        (["power bi", "data analyst", "business analyst"], "power bi data analytics playlist"),
        (["frontend", "html", "css", "javascript"], "frontend web development playlist"),
        (["backend", "api", "fastapi"], "backend development api playlist"),
        (["cloud", "devops", "aws", "docker", "kubernetes"], "cloud devops aws playlist"),
        (["digital marketing", "seo", "social media"], "digital marketing playlist"),
        (["ui", "ux", "figma", "product design"], "ui ux design playlist"),
        (["finance", "accounting", "investment"], "finance and accounting playlist"),
        (["communication", "leadership", "management"], "communication and leadership playlist"),
    ]

    queries: List[str] = []
    for keywords, query in query_map:
        if any(keyword in lower for keyword in keywords):
            queries.append(query)

    if not queries:
        queries = [
            "career roadmap skills playlist",
            "job ready portfolio projects playlist",
        ]

    return queries[:5]


def _fetch_youtube_playlists(queries: List[str], max_results: int) -> List[YouTubePlaylist]:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="YouTube API is not configured. Add YOUTUBE_API_KEY in .env",
        )

    collected: List[YouTubePlaylist] = []
    seen_ids = set()
    per_query = max(3, min(10, max_results))

    for query in queries:
        params = urlencode(
            {
                "part": "snippet",
                "type": "playlist",
                "maxResults": per_query,
                "q": query,
                "key": api_key,
            }
        )
        url = f"https://www.googleapis.com/youtube/v3/search?{params}"

        try:
            with urlopen(url, timeout=12) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"YouTube API request failed: {exc}")

        items = payload.get("items", [])
        for item in items:
            playlist_id = item.get("id", {}).get("playlistId")
            snippet = item.get("snippet", {})
            if not playlist_id or playlist_id in seen_ids:
                continue

            seen_ids.add(playlist_id)
            collected.append(
                YouTubePlaylist(
                    title=snippet.get("title", "Untitled Playlist"),
                    url=f"https://www.youtube.com/playlist?list={playlist_id}",
                    channel=snippet.get("channelTitle"),
                    description=snippet.get("description", ""),
                    thumbnail=(
                        (snippet.get("thumbnails", {}).get("medium") or {}).get("url")
                        or (snippet.get("thumbnails", {}).get("default") or {}).get("url")
                    ),
                )
            )
            if len(collected) >= max_results:
                return collected

    return collected


@app.on_event("startup")
def startup() -> None:
    try:
        _set_rag_state(_init_rag(), None)
    except Exception as exc:
        _set_rag_state(None, str(exc))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    return {
        "ready": app.state.rag is not None,
        "error": app.state.init_error,
    }


@app.post("/vector-store/load")
def load_vector_store():
    try:
        rag = _init_rag()
        _set_rag_state(rag, None)
        return {"status": "loaded"}
    except Exception as exc:
        _set_rag_state(None, str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/vector-store/create")
def create_vector_store():
    try:
        rag = CareerRAG()
        rag.create_vector_store()
        rag.save_vector_store()
        _set_rag_state(rag, None)
        return {"status": "created"}
    except Exception as exc:
        _set_rag_state(None, str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/recommend/structured", response_model=RecommendResponse)
def recommend_structured(payload: StructuredProfileRequest):
    rag = _get_rag()
    user_profile = (
        f"Education: {payload.degree} in {payload.branch}\n"
        f"Experience: {payload.experience} years ({payload.experience_type})\n"
        f"Skills: {payload.skills}\n"
        f"Interests: {payload.interests}"
    )
    api_key = os.getenv("GROQ_API_KEY")
    recommendation, confidence = rag.recommend_career(user_profile, api_key=api_key)
    similar = _similar_docs(rag, user_profile, top_k=3)
    return RecommendResponse(
        recommendation=recommendation,
        confidence=float(confidence),
        similar=similar,
    )


@app.post("/recommend/natural", response_model=RecommendResponse)
def recommend_natural(payload: NaturalProfileRequest):
    rag = _get_rag()
    api_key = os.getenv("GROQ_API_KEY")
    recommendation, confidence = rag.recommend_career(payload.description, api_key=api_key)
    similar = _similar_docs(rag, payload.description, top_k=3)
    return RecommendResponse(
        recommendation=recommendation,
        confidence=float(confidence),
        similar=similar,
    )


@app.post("/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest):
    rag = _get_rag()
    api_key = os.getenv("GROQ_API_KEY")
    recommendation, confidence = rag.recommend_career(payload.query, api_key=api_key)
    similar = _similar_docs(rag, payload.query, top_k=3)
    return RecommendResponse(
        recommendation=recommendation,
        confidence=float(confidence),
        similar=similar,
    )


@app.post("/similar", response_model=List[SimilarDoc])
def similar(payload: RecommendRequest):
    rag = _get_rag()
    return _similar_docs(rag, payload.query, top_k=3)


@app.post("/recommend/resume", response_model=RecommendResponse)
def recommend_resume(file: UploadFile = File(...)):
    rag = _get_rag()
    resume_text = _extract_resume_text(file)
    api_key = os.getenv("GROQ_API_KEY")
    recommendation, confidence = rag.recommend_career(resume_text, api_key=api_key)
    similar = _similar_docs(rag, resume_text, top_k=3)
    return RecommendResponse(
        recommendation=recommendation,
        confidence=float(confidence),
        similar=similar,
    )


@app.post("/youtube/playlists", response_model=List[YouTubePlaylist])
def youtube_playlists(payload: PlaylistSuggestionRequest):
    queries = _build_youtube_queries_from_recommendation(payload.recommendation)
    return _fetch_youtube_playlists(queries, max_results=payload.max_results)


if os.path.isdir(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/")
def home():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.isfile(index_path):
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


#python -m uvicorn api:app --host 127.0.0.1 --port 8000
