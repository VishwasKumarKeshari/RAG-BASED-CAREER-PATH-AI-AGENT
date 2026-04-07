import os
from typing import List, Tuple

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from groq import Groq
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    context_found: bool
    sources: List[str]


class CareerChatRAG:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            collection_name="career_knowledge_base",
            embedding_function=self.embeddings_model,
            persist_directory=persist_directory,
        )

    def retrieve_context(
        self, question: str, top_k: int = 4
    ) -> List[Tuple[Document, float]]:
        return self.vector_store.similarity_search_with_score(question, k=top_k)

    def answer(self, question: str) -> ChatResponse:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="GROQ_API_KEY is missing. Add it to .env to use chat.",
            )

        try:
            client = Groq(api_key=api_key)
            docs_and_scores = self.retrieve_context(question, top_k=4)

            # Chroma score is distance-like (lower is usually better).
            relevant = [(doc, score) for doc, score in docs_and_scores if score <= 1.2]

            if relevant:
                context = "\n\n".join(doc.page_content for doc, _ in relevant[:3])
                sources = sorted(
                    {
                        doc.metadata.get("source", "unknown")
                        for doc, _ in relevant[:3]
                        if isinstance(doc.metadata, dict)
                    }
                )
                prompt = f"""You are a helpful career assistant.
Use the retrieved context as primary grounding. If needed, you may add brief general knowledge.

Question:
{question}

Retrieved Context:
{context}

Provide a concise, practical response with clear next steps."""
                context_found = True
            else:
                # Fallback for general questions when no strong KB match is found.
                sources = []
                prompt = f"""You are a helpful AI assistant.
Answer the user's question clearly and accurately using your general knowledge.
If the question is career-related, keep it practical and actionable.

Question:
{question}"""
                context_found = False

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            answer = (response.choices[0].message.content or "").strip()
            if not answer:
                answer = "I could not generate an answer right now. Please try again."
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Chat generation failed: {exc}")

        return ChatResponse(answer=answer, context_found=context_found, sources=sources)


_chat_service: CareerChatRAG | None = None


def _get_chat_service() -> CareerChatRAG:
    global _chat_service
    if _chat_service is None:
        _chat_service = CareerChatRAG()
    return _chat_service


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    service = _get_chat_service()
    return service.answer(payload.question)
