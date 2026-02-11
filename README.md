# Career Compass - RAG Career Recommendation API

This project provides a FastAPI backend with a frontend UI for AI-powered career recommendations using a RAG pipeline.

## Stack
- FastAPI
- Groq API
- LangChain + ChromaDB
- Sentence Transformers
- Plain HTML/CSS/JS frontend (`frontend/`)

## Prerequisites
- Python 3.8+
- `GROQ_API_KEY` in `.env`

Example `.env`:
```env
GROQ_API_KEY=your_actual_api_key_here
```

## Run Locally
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the app:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

3. Open:
- App UI: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`

## Key Endpoints
- `GET /health`
- `GET /status`
- `POST /recommend`
- `POST /recommend/natural`
- `POST /recommend/structured`
- `POST /recommend/resume`
- `POST /similar`
- `POST /vector-store/load`
- `POST /vector-store/create`

## Project Structure
- `api.py`: FastAPI server and routes
- `rag.py`: RAG pipeline and retrieval/recommendation logic
- `frontend/`: Static web UI
- `data/`: Career knowledge base files
- `chroma_db/`: Persisted vector store

## Notes
- The frontend is served by FastAPI at `/` and static assets under `/frontend`.
