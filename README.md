#  RAG-Based Career Path AI Agent

An intelligent career recommendation system powered by **Google Gemini AI**, **ChromaDB vector database**, and **Retrieval-Augmented Generation (RAG)** technology. This system provides personalized career guidance by analyzing user skills, interests, and preferences against a comprehensive knowledge base of 100 career paths across 10 diverse categories.

![Career Compass](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=google)
![RAG System](https://img.shields.io/badge/RAG-Technology-green?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/Vector-DB-orange?style=for-the-badge&logo=chroma)

##  Key Features

###  AI-Powered Intelligence
- **Google Gemini AI** for natural language understanding and personalized recommendations
- **Context-aware responses** that consider user background, skills, and career goals
- **Intelligent reasoning** with step-by-step career guidance

###  Advanced Retrieval System
- **ChromaDB vector database** for efficient similarity search
- **Sentence Transformers** (all-MiniLM-L6-v2) for high-quality embeddings
- **Semantic search** that understands meaning, not just keywords

###  Comprehensive Career Database
- **100 career paths** across 10 major categories
- **Detailed profiles** including skills, education, salary, and growth paths
- **Real-time matching** with confidence scoring

###  User-Friendly Interface
- **Streamlit web application** with intuitive design
- **Dual input modes**: Structured forms and natural language
- **Interactive recommendations** with detailed explanations

###  Modular Architecture
- **Separation of concerns** with dedicated functions for each pipeline step
- **Step-wise API integration** (API keys only needed for LLM generation)
- **Persistent vector storage** with automatic ChromaDB management

##  Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get free key](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   `ash
   git clone <your-repo-url>
   cd "RAG BASED CAREER PATH AI AGENT"
   `

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
RAG BASED CAREER PATH AI AGENT/
  app_gemini.py              # Streamlit web interface
  rag_gemini.py              # RAG pipeline implementation
  requirements.txt           # Python dependencies
  README.md                  # Project documentation
  .gitignore                 # Git ignore rules
  .streamlit/                # Streamlit configuration
     secrets.toml          # API keys (create this file)
  data/                     # Career knowledge base
     business_finance.txt
     creative_design.txt
     data_science_ml.txt
     education_research.txt
     engineering.txt
     healthcare_medical.txt
     legal_hr.txt
     marketing_sales.txt
     operations_logistics.txt
     software_development.txt
  chroma_db/               # ChromaDB vector database
     chroma.sqlite3       # Database metadata
     [collection_id]/     # Vector data files
  __pycache__/             # Python cache (ignored)
`

##  System Architecture

### RAG Pipeline Flow
`
User Input (Skills/Interests/Description)
          
          
    
      Document       
      Loading          data/*.txt files
    
          
          
    
      Text Chunking    RecursiveCharacterTextSplitter
    
          
          
    
      Embedding        Sentence Transformers
      Generation          (all-MiniLM-L6-v2)
    
          
          
    
      Vector Storage   ChromaDB
    
          
          
    
      Similarity     
      Search           Cosine similarity
    
          
          
    
      Context        
      Building         Top-k relevant careers
    
          
          
    
      Gemini AI        Personalized
      Generation          recommendations
    
          
          
     Final Recommendation + Confidence Scores
`

##  Core Components

### ag_gemini.py - RAG Pipeline Engine

**Modular Functions:**
- load_documents() - Load raw career documents from TXT files
- chunk_documents() - Split documents into manageable chunks
- create_vector_store() - Generate embeddings and store in ChromaDB
- load_knowledge_base() - Combined loading + chunking (backward compatibility)
- etrieve_similar_documents() - Semantic search with similarity scores
- ecommend_career() - Generate personalized recommendations via Gemini AI

**Key Classes:**
- CareerRAG - Main orchestrator class with complete pipeline management

### pp_gemini.py - Streamlit Web Interface

**Features:**
- **Structured Input Mode**: Form-based input for degree, skills, experience
- **Natural Language Mode**: Free-text description of interests and goals
- **Real-time Processing**: Instant recommendations with loading indicators
- **Confidence Visualization**: Match percentages and similar career suggestions
- **Responsive Design**: Mobile-friendly interface

### data/ Directory - Career Knowledge Base

**10 Career Categories with 10 careers each:**
1. ** Business & Finance** (Accountant, Financial Analyst, Investment Banker, etc.)
2. ** Creative & Design** (Graphic Designer, UX/UI Designer, Illustrator, etc.)
3. ** Data Science & ML** (Data Scientist, ML Engineer, Data Analyst, etc.)
4. ** Education & Research** (Teacher, Professor, Researcher, etc.)
5. ** Engineering** (Mechanical Engineer, Civil Engineer, Electrical Engineer, etc.)
6. ** Healthcare & Medical** (Doctor, Nurse, Pharmacist, etc.)
7. ** Legal & HR** (Lawyer, HR Manager, Compliance Officer, etc.)
8. ** Marketing & Sales** (Marketing Manager, Sales Representative, etc.)
9. ** Operations & Logistics** (Supply Chain Manager, Operations Manager, etc.)
10. ** Software Development** (Full Stack Developer, DevOps Engineer, etc.)

**Career Profile Structure:**
- **Career Title** and comprehensive description
- **Required Skills** and technical competencies
- **Education Requirements** and qualifications
- **Salary Range** and compensation insights
- **Career Growth Path** and advancement opportunities

##  Technical Specifications

### Dependencies
`
streamlit>=1.28.0          # Web interface
google-generativeai>=0.3.0  # Gemini AI integration
langchain-chroma>=0.1.0     # ChromaDB integration
langchain-huggingface>=0.0.3 # HuggingFace embeddings
sentence-transformers>=2.2.0 # Text embeddings
chromadb>=0.4.0            # Vector database
`

### Vector Database Configuration
- **Database**: ChromaDB with SQLite backend
- **Collection**: career_knowledge_base
- **Embedding Model**: ll-MiniLM-L6-v2 (384-dimensional vectors)
- **Chunk Size**: 1000 characters with 200-character overlap
- **Similarity Metric**: Cosine similarity

### API Integration
- **Provider**: Google Gemini AI
- **Model**: gemini-pro (with fallback to gemini-flash-latest)
- **API Key Management**: Streamlit secrets (.streamlit/secrets.toml)
- **Step-wise Integration**: API key only accessed during LLM generation

##  Performance Metrics

- **Initialization Time**: ~5-10 seconds (first run downloads embeddings)
- **Recommendation Time**: ~2-4 seconds (including API latency)
- **Vector Search**: <50ms for similarity matching
- **Memory Usage**: ~500MB (embeddings model + ChromaDB)
- **Storage**: ~50MB (vector database + career data)

##  Deployment Options

### Streamlit Cloud (Recommended)
1. Push repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Set main file: pp_gemini.py
5. Add secret: GEMINI_API_KEY = "your_key_here"
6. Deploy!

### Local Deployment
`ash
# Install dependencies
pip install -r requirements.txt

# Set up secrets
mkdir .streamlit
echo "GEMINI_API_KEY = \"your_key_here\"" > .streamlit/secrets.toml

# Run application
streamlit run app_gemini.py
`

### Docker Deployment
`dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app_gemini.py", "--server.port=8501", "--server.address=0.0.0.0"]
`

##  Security & Best Practices

### API Key Management
- API keys stored in .streamlit/secrets.toml (never committed)
- Environment variable fallback for development
- No sensitive data in application code

### Data Privacy
- All processing happens locally (except Gemini API calls)
- User inputs not stored or logged
- Career database is static and publicly available

### Git Security
- .gitignore excludes secrets, cache, and large files
- Never commit API keys or sensitive credentials
- Use environment variables for production deployments

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Run pip install -r requirements.txt |
| GEMINI_API_KEY not found | Check .streamlit/secrets.toml exists |
| ChromaDB connection error | Delete chroma_db/ folder and restart |
| Slow first run | Downloading embeddings model (~100MB) |
| Rate limiting | Gemini free tier: 60 requests/minute |
| Memory errors | Reduce chunk size in ag_gemini.py |

##  Contributing

### Adding New Careers
1. Choose appropriate category file in data/
2. Add career profile using this format:
   `
   Career Name Career Path:
   [Description]

   Skills: [skill1, skill2, skill3]
   Education: [requirements]
   Experience: [level needed]
   Salary: [range]
   Growth: [advancement opportunities]

   ---
   `
3. Test with python rag_gemini.py
4. Commit and push changes

### Code Improvements
1. Fork the repository
2. Create feature branch: git checkout -b feature-name
3. Make changes and test thoroughly
4. Submit pull request with detailed description

##  Future Enhancements

- [ ] **Multi-language support** for global accessibility
- [ ] **Advanced filtering** by location, salary, remote work
- [ ] **Career transition planning** with skill gap analysis
- [ ] **Integration with job boards** for real-time opportunities
- [ ] **User feedback system** for continuous improvement
- [ ] **Mobile app version** using Streamlit mobile features

##  License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute!

##  Acknowledgments

- **Google Gemini AI** for powerful language understanding
- **ChromaDB** for efficient vector database management
- **Sentence Transformers** for high-quality text embeddings
- **LangChain** for RAG pipeline framework
- **Streamlit** for intuitive web interface

##  Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: This README and inline code comments

---

**Ready to discover your ideal career path?** 

`ash
streamlit run app_gemini.py
`

*Powered by AI, driven by your potential!* 
