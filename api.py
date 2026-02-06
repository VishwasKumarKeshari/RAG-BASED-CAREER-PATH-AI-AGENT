import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag import CareerRAG

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(title="Career Compass RAG API", version="1.0.0")


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


def _init_rag() -> CareerRAG:
    rag = CareerRAG()
    try:
        rag.load_vector_store()
    except Exception:
        rag.create_vector_store()
        rag.save_vector_store()
    return rag


def _get_rag() -> CareerRAG:
    rag = getattr(app.state, "rag", None)
    if rag is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
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


@app.on_event("startup")
def startup() -> None:
    try:
        app.state.rag = _init_rag()
        app.state.init_error = None
    except Exception as exc:
        app.state.rag = None
        app.state.init_error = str(exc)


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
        app.state.rag = rag
        app.state.init_error = None
        return {"status": "loaded"}
    except Exception as exc:
        app.state.rag = None
        app.state.init_error = str(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/vector-store/create")
def create_vector_store():
    try:
        rag = CareerRAG()
        rag.create_vector_store()
        rag.save_vector_store()
        app.state.rag = rag
        app.state.init_error = None
        return {"status": "created"}
    except Exception as exc:
        app.state.rag = None
        app.state.init_error = str(exc)
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
