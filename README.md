# 🎯 Career Compass - AI-Powered Career Recommendations

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/VishwasKumarKeshari/RAG-BASED-CAREER-PATH-AI-AGENT)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

An intelligent career recommendation system powered by **Google Gemini AI** and **Retrieval-Augmented Generation (RAG)**. Get personalized career suggestions based on your skills, interests, and background using advanced AI and semantic search.

## 🌟 Features

✅ **AI-Powered Recommendations** - Uses Google Gemini AI for intelligent, context-aware career suggestions  
✅ **Semantic Search** - Retrieves relevant careers using advanced embeddings (Sentence Transformers)  
✅ **Two Input Modes**:
   - 📋 **Structured**: Fill form with degree, branch, skills, experience
   - 📝 **Natural Language**: Describe yourself freely  
✅ **Confidence Scoring** - See match percentages for each recommended career  
✅ **100+ Career Profiles** - Comprehensive knowledge base covering diverse roles across 10 categories  
✅ **Real-time Processing** - Instant recommendations with detailed reasoning  
✅ **Modular Architecture** - Clean, maintainable code with separate RAG pipeline  

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key (free at [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VishwasKumarKeshari/RAG-BASED-CAREER-PATH-AI-AGENT.git
   cd "RAG BASED CAREER PATH AI AGENT"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   Create a `.streamlit/secrets.toml` file:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```

5. **Launch the application**
   ```bash
   streamlit run app_gemini.py
   ```

6. **Open your browser**
   Navigate to: `http://localhost:8501`

2. **Create virtual environment**
   `ash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   `

3. **Install dependencies**
   `ash
   pip install -r requirements.txt
   `

4. **Configure API key**
   Create a .streamlit/secrets.toml file:
   `	oml
   GEMINI_API_KEY = "your_actual_api_key_here"
   `

5. **Launch the application**
   `ash
   streamlit run app_gemini.py
   `

6. **Open your browser**
   Navigate to: http://localhost:8501

##  Project Structure

`
career-detection/
 app_gemini.py                 # Main Streamlit web interface
 rag_gemini.py                 # RAG pipeline with Gemini AI
 career_knowledge_base.py      # Career data processing utilities
 data/                         # Career knowledge base (10 categories)
    technology.txt
    healthcare.txt
    finance.txt
    ...
 chroma_db/                    # Vector database storage
 requirements.txt              # Python dependencies
 .streamlit/
    secrets.toml              # API keys (gitignored)
 README.md
`

##  System Architecture

### RAG Pipeline Flow
`
User Input
    
[Document Loading] (Load career knowledge base)
    
[Text Chunking] (Split into manageable chunks)
    
[Embedding Generation] (Sentence Transformers: all-MiniLM-L6-v2)
    
[Vector Storage] (ChromaDB for persistence)
    
[Semantic Search] (Cosine similarity retrieval)
    
[Context Building] (Combine user input + relevant careers)
    
[Gemini API Call] (gemini-pro model for generation)
    
[Personalized Recommendation] (With reasoning & next steps)
`

##  Core Components

### 
ag_gemini.py - RAG Pipeline
- CareerRAG class: Main orchestrator for the RAG system
- load_documents(): Loads and processes career data from multiple files
- chunk_documents(): Splits documents into optimal chunks for embedding
- create_vector_store(): Generates embeddings and stores in ChromaDB
- 
etrieve_similar_documents(): Performs semantic search for relevant careers

### pp_gemini.py - Streamlit Interface
- Dual input modes: Structured form and natural language
- Real-time recommendations with loading indicators
- Confidence scores and career match percentages
- Responsive design with clean UI

### Career Knowledge Base
- **10 Categories**: Technology, Healthcare, Finance, Education, etc.
- **100+ Career Profiles**: Comprehensive information for each role
- **Structured Data**: Skills, education, salary ranges, growth paths
- **Modular Organization**: Easy to add new careers and categories

##  Career Categories

1. **Technology** - Software Development, Data Science, DevOps
2. **Healthcare** - Medical, Nursing, Healthcare Administration  
3. **Finance** - Banking, Investment, Financial Analysis
4. **Education** - Teaching, Educational Administration
5. **Engineering** - Civil, Mechanical, Electrical Engineering
6. **Creative** - Design, Marketing, Content Creation
7. **Business** - Management, Consulting, Entrepreneurship
8. **Legal** - Law, Compliance, Legal Services
9. **Science** - Research, Laboratory Work, Scientific Analysis
10. **Trades** - Skilled Trades, Technical Services

##  Security & Configuration

- API keys stored in .streamlit/secrets.toml (never committed)
- .gitignore excludes sensitive files and cache directories
- Environment-based configuration for different deployment scenarios

##  Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**
   `ash
   git add .
   git commit -m "AI Career Recommendation System with RAG"
   git push origin main
   `

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file path: pp_gemini.py
   - Add environment secrets:
     `
     GEMINI_API_KEY = your_api_key_here
     `

3. **Access your live application!**

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| GEMINI_API_KEY not found | Check .streamlit/secrets.toml has your API key |
| ModuleNotFoundError | Run pip install -r requirements.txt |
| Rate limiting | Free tier has limits; consider upgrading or wait |
| Slow first run | Downloads embedding model (~100MB) on first use |
| Database errors | Delete chroma_db/ folder and restart |

##  API & Dependencies

### Google Gemini AI
- **Model**: gemini-pro
- **Free Tier**: 60 queries/minute
- **Setup**: [Google AI Studio](https://makersuite.google.com/app/apikey)

### Key Libraries
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: ll-MiniLM-L6-v2 for embeddings
- **LangChain**: Text processing and document chunking
- **Streamlit**: Web application framework

##  Performance Metrics

- **Recommendation Time**: ~3-8 seconds (including API latency)
- **Embedding Generation**: ~2 seconds (first run, cached after)
- **Vector Search**: <200ms (across 100+ careers)
- **Memory Usage**: ~500MB (with loaded models)

##  Contributing

Want to expand the career knowledge base?

1. **Add New Careers**: Edit files in data/ directory
2. **Follow Format**: Use consistent structure with --- separators
3. **Test Changes**: Run python rag_gemini.py to validate
4. **Submit PR**: Push changes and create pull request

##  License

This project is open source under the MIT License. Feel free to use, modify, and distribute!

##  Acknowledgments

- **Google Gemini AI** for powerful language generation
- **ChromaDB** for efficient vector storage
- **Sentence Transformers** for high-quality embeddings
- **Streamlit** for the amazing web app framework

---

**Ready to discover your ideal career path?** 

Run streamlit run app_gemini.py and start your journey!
