# 🎯 Career Compass - AI-Powered Career Recommendations# Career Compass — AI-Powered Career Path Detector



An intelligent career recommendation system powered by **Google Gemini AI** and **Retrieval-Augmented Generation (RAG)**.This repository contains a small prototype app that suggests career paths based on structured inputs (degree, branch, skills) and natural-language descriptions.



## 🌟 FeaturesContents

- `app.py` — Streamlit app UI (Structured input + Natural Language matcher).

✅ **AI-Powered Recommendations** - Uses Gemini AI for intelligent, context-aware career suggestions  - `api.py` — (optional) FastAPI server example (not included by default).

✅ **Semantic Search** - Retrieves relevant careers using advanced embeddings (sentence-transformers)  - `train_model.py` — Trains a scikit-learn Pipeline and saves it to `models/career_classifier.pkl`.

✅ **Two Input Modes**:- `nlp_module.py` — NLP matcher using `sentence-transformers`.

   - 📋 **Structured**: Fill form with degree, branch, skills, experience- `utils.py` — helper functions used by the training pipeline.

   - 📝 **Natural Language**: Describe yourself freely- `data/careers.csv` — small example dataset.

- `resources/resources.json` — learning resources mapped to careers.

✅ **Confidence Scoring** - See match percentages for each recommended career  

✅ **15+ Career Profiles** - Comprehensive knowledge base covering diverse roles  Quickstart (local)

1. Create a virtual environment (recommended):

## 📋 Prerequisites

```powershell

- Python 3.8+python -m venv .venv

- Google Gemini API key (free at https://makersuite.google.com/app/apikey).\.venv\Scripts\Activate.ps1

```

## 🚀 Quick Start

2. Install dependencies:

### 1. Install Dependencies

```bash```powershell

pip install -r requirements.txtpip install -r requirements.txt

``````



### 2. Add Your Gemini API Key3. Train the pipeline (creates `models/career_classifier.pkl`):

Create/update `.env` file:

``````powershell

GEMINI_API_KEY=your_actual_api_key_herepython train_model.py

``````



### 3. Test the RAG Pipeline4. Run the Streamlit app:

```bash

python rag_gemini.py```powershell

```streamlit run app.py

```

Expected output:

- ✅ Gemini RAG initializedNotes

- ✅ Knowledge base loaded (15 careers)- Do NOT commit large binaries (like `models/`) unless you intentionally want to store them in Git LFS. By default `models/` is ignored in `.gitignore`.

- ✅ Sample recommendation generated- The NLP matcher uses `sentence-transformers` which will download model weights on first run — that may take time and require more disk space.

- ✅ Similar careers retrieved with scores- This repo uses a small synthetic dataset for demonstration. For real use, expand `data/careers.csv` with more examples.



### 4. Launch the Web AppDeploying

```bash- To deploy on Streamlit Community Cloud: push this repository to GitHub, then create a new app on share.streamlit.io pointing to `app.py` and the branch you pushed.

streamlit run app_gemini.py- If you prefer a backend API, consider using FastAPI and deploy on Render/Railway/Heroku.

```

Security

Then open: **http://localhost:8501**- The trained pipeline is pickled with `joblib`. Only load pickles you trust.



## 📁 Project StructureLicense & Credits

## 📁 Project Structure

```
career-detection/
├── app_gemini.py                 # Main Streamlit web interface
├── rag_gemini.py                 # RAG pipeline with Gemini AI
├── data/
│   └── career_knowledge_base.txt # Career documents & data (15 careers)
├── requirements.txt              # Python dependencies
├── .env                          # API keys (gitignored)
└── .gitignore                    # Git configuration
```

## 🔧 System Architecture

### RAG Pipeline Flow
```
User Input
    ↓
[Embedding] (sentence-transformers: all-MiniLM-L6-v2)
    ↓
[Vector Search] (cosine similarity search)
    ↓
[Retrieve Top-3 Careers] (from 15-career knowledge base)
    ↓
[Build Context Prompt] (combine user input + career info)
    ↓
[Gemini API Call] (gemini-pro model)
    ↓
[Generate Recommendation] (with reasoning & next steps)
    ↓
Display Result + Confidence Score
```

## 📊 Core Components

### `rag_gemini.py` - RAG Pipeline
- `CareerRAG` class: Main orchestrator
- `create_knowledge_base()`: Loads 15 careers + generates embeddings
- `retrieve_similar_careers()`: Semantic search for matching careers
- `recommend_career()`: Calls Gemini API for personalized recommendations

### `data/career_knowledge_base.txt` - Knowledge Base
- 15 comprehensive career documents in structured text format
- Each career includes: description, skills, education, salary, growth path
- Source of truth for career information
- Separated by `---` delimiters for easy parsing

### `app_gemini.py` - Streamlit UI
- Two interaction modes (Structured & Natural Language)
- Real-time recommendations
- Confidence scores & similar career suggestions

## 🎯 Career Profiles Included

1. Data Scientist
2. Machine Learning Engineer
3. Web Developer
4. DevOps Engineer
5. Cloud Architect
6. Mobile Developer
7. UI/UX Designer
8. Cybersecurity Analyst
9. Business Analyst
10. Database Administrator
11. Backend Engineer
12. Frontend Developer
13. Full Stack Developer
14. Solutions Architect
15. Product Manager

## 🔐 Security

- API key stored in `.env` (never committed to git)
- `.gitignore` excludes `.env`, `models/`, `__pycache__/`
- No sensitive data in code

## 📡 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Gemini RAG career recommendation system"
   git push
   ```

2. **Go to** https://share.streamlit.io

3. **Deploy new app**:
   - Select your GitHub repo
   - Choose `app_gemini.py` as main file
   - Add secret in app settings:
     ```
     GEMINI_API_KEY = your_key_here
     ```

4. **Access** your live app!

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY not found` | Check `.env` file has your API key |
| `ModuleNotFoundError: google` | Run `pip install google-generativeai` |
| `ModuleNotFoundError: sentence_transformers` | Run `pip install sentence-transformers` |
| Rate limiting | Gemini free tier has limits; wait and retry |
| Slow recommendations | First run downloads embeddings model (~100MB) |

## 🌐 API Documentation

### Google Gemini
- **Model**: `gemini-pro`
- **Free Tier**: 60 queries/minute
- **Get Key**: https://makersuite.google.com/app/apikey

### Sentence Transformers
- **Model**: `all-MiniLM-L6-v2`
- **Embedding Dim**: 384
- **Local**: No API calls (fully offline after download)

## 📈 Performance

- **Recommendation Time**: ~2-5 seconds (including Gemini API latency)
- **Embedding Generation**: ~1 second (first run, cached after)
- **Vector Search**: <100ms (15 careers)

## 🤝 Contributing

Want to add more careers or features?
1. Edit `data/career_knowledge_base.txt` to add career documents (use `---` separators)
2. Test with `python rag_gemini.py`
3. Push to GitHub!

## 📝 License

This project is open source. Feel free to use and modify!

---

**Questions?** Check `GEMINI_SETUP.md` for detailed setup troubleshooting.

**Ready to explore careers?** Run `streamlit run app_gemini.py` 🚀
