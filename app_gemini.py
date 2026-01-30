import streamlit as st
from rag_gemini import CareerRAG
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

st.set_page_config(page_title="Career Compass - Groq RAG", layout="wide")
st.title("🎯 Career Compass — AI-Powered Career Recommendations")
st.markdown("*Powered by Groq AI and RAG Technology*")

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
    st.session_state.initialized = False

# Initialize RAG system
@st.cache_resource
def initialize_rag():
    """Initialize RAG pipeline with Gemini"""
    try:
        # Instantiate RAG system (no API key needed for retrieval)
        rag = CareerRAG()

        # Try to load existing vector store first
        try:
            rag.load_vector_store()
            print("📂 Loaded existing vector store with 100 career paths")
        except Exception:
            print("📚 Creating new vector store from 100 career paths...")
            rag.create_vector_store()
            rag.save_vector_store()

        return rag, None
    except Exception as e:
        return None, str(e)

# Load RAG
rag_system, error = initialize_rag()

if error or rag_system is None:
    st.error(f"❌ Failed to initialize RAG: {error or 'Unknown error'}")
else:
    st.success("✅ RAG System Ready")
    
    # Sidebar
    st.sidebar.header("🚀 Career Discovery")
    mode = st.sidebar.radio("Select Mode", ["Structured Profile", "Natural Language"])
    
    if mode == "Structured Profile":
        st.subheader("📋 Tell us about yourself")
        
        col1, col2 = st.columns(2)
        with col1:
            degree = st.selectbox("Education", ["B.Tech", "B.Sc", "B.Des", "MBA", "M.Tech", "Diploma"])
            branch = st.selectbox("Branch/Field", ["CSE", "IT", "ECE", "Mechanical", "Civil", "Design", "Management", "Other"])
        
        with col2:
            experience = st.slider("Years of Experience", 0, 20, 0)
            experience_type = st.selectbox("Experience Type", ["No experience", "Internship", "Full-time", "Freelance", "Mixed"])
        
        skills = st.text_area("Your Skills (comma or pipe separated)", placeholder="e.g., Python, Machine Learning, SQL, Cloud")
        interests = st.text_area("Interests & Goals", placeholder="e.g., AI/ML, Data Science, Infrastructure, Security, Web Development")
        
        if st.button("🔍 Get Career Recommendation", use_container_width=True):
            if skills and interests:
                user_profile = f"""
                Education: {degree} in {branch}
                Experience: {experience} years ({experience_type})
                Skills: {skills}
                Interests: {interests}create
                """
                
                with st.spinner("🤖 Groq is analyzing your profile..."):
                    try:
                        api_key = os.getenv("GROQ_API_KEY")
                        recommendation, confidence = rag_system.recommend_career(user_profile, api_key=api_key)
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown("### 💼 Personalized Recommendation")
                        with col2:
                            st.metric("Confidence", f"{confidence:.0%}")
                        
                        st.write(recommendation)
                        
                        # Show similar careers
                        st.markdown("---")
                        st.markdown("### 🔗 Related Career Paths")
                        
                        similar = rag_system.retrieve_similar_documents(user_profile, top_k=3)
                        for i, (doc, score) in enumerate(similar, 1):
                            with st.expander(f"Career {i} (Match: {score:.0%})"):
                                st.write(doc.page_content)
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please fill in both skills and interests")
    
    else:  # Natural Language mode
        st.subheader("📝 Describe Your Career Journey")
        
        user_description = st.text_area(
            "Tell us about yourself",
            placeholder="E.g., I'm passionate about solving problems with AI. I have 3 years Python experience and built several ML models. I want to work on impactful products and grow my leadership skills...",
            height=150
        )
        
        if st.button("✨ Find Your Career Path", use_container_width=True):
            if user_description:
                with st.spinner("🤖 Groq is analyzing your profile..."):
                    try:
                        api_key = os.getenv("GROQ_API_KEY")
                        recommendation, confidence = rag_system.recommend_career(user_description, api_key=api_key)
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown("### 💼 Your Ideal Career Path")
                        with col2:
                            st.metric("Confidence", f"{confidence:.0%}")
                        
                        st.write(recommendation)
                        
                        # Show matching careers
                        st.markdown("---")
                        st.markdown("### 🎯 Matching Opportunities")
                        
                        similar = rag_system.retrieve_similar_documents(user_description, top_k=3)
                        for i, (doc, score) in enumerate(similar, 1):
                            with st.expander(f"Opportunity {i} (Match: {score:.0%})"):
                                st.write(doc.page_content)
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please describe your background and interests")

st.markdown("---")
st.markdown("""
### ℹ️ About This RAG System
This application uses **Retrieval-Augmented Generation (RAG)** with Groq AI:

🔍 **Step 1 - User Query → Retriever**: Your input goes to the retriever  
🗄️ **Step 2 - Retriever → Vector Store**: Searches 100 career paths for matches  
🤖 **Step 3 - Context + Prompt → LLM**: Groq AI gets relevant careers + your query  
✨ **Step 4 - LLM → Output**: Generates personalized career recommendations  

**Technology Stack**: Groq AI + Sentence Transformers + FAISS Vector Store + 100 Career Paths
""")
