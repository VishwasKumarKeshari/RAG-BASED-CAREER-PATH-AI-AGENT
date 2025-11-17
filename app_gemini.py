import streamlit as st
import os
from rag_gemini import CareerRAG
from career_knowledge_base import get_career_documents

st.set_page_config(page_title="Career Compass - Gemini RAG", layout="wide")
st.title("🎯 Career Compass — AI-Powered Career Recommendations")
st.markdown("*Powered by Google Gemini AI and RAG Technology*")

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
    st.session_state.initialized = False

# Initialize RAG system
@st.cache_resource
def initialize_rag():
    """Initialize RAG pipeline with Gemini"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None, "GEMINI_API_KEY not found"
        
        rag = CareerRAG(api_key=api_key)
        docs = get_career_documents()
        rag.create_knowledge_base(docs)
        return rag, None
    except Exception as e:
        return None, str(e)

# Load RAG
rag_system, error = initialize_rag()

if error or rag_system is None:
    st.error(f"❌ Failed to initialize RAG: {error or 'Unknown error'}")
    st.info("ℹ️ Make sure GEMINI_API_KEY environment variable is set")
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
                Interests: {interests}
                """
                
                with st.spinner("🤖 Gemini is analyzing your profile..."):
                    try:
                        recommendation, confidence = rag_system.recommend_career(user_profile)
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown("### 💼 Personalized Recommendation")
                        with col2:
                            st.metric("Confidence", f"{confidence:.0%}")
                        
                        st.write(recommendation)
                        
                        # Show similar careers
                        st.markdown("---")
                        st.markdown("### 🔗 Related Career Paths")
                        
                        similar = rag_system.retrieve_similar_careers(user_profile, top_k=3)
                        for i, (career_info, score) in enumerate(similar, 1):
                            with st.expander(f"Career {i} (Match: {score:.0%})"):
                                st.write(career_info)
                    
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
                with st.spinner("🤖 Gemini is analyzing your profile..."):
                    try:
                        recommendation, confidence = rag_system.recommend_career(user_description)
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown("### 💼 Your Ideal Career Path")
                        with col2:
                            st.metric("Confidence", f"{confidence:.0%}")
                        
                        st.write(recommendation)
                        
                        # Show matching careers
                        st.markdown("---")
                        st.markdown("### 🎯 Matching Opportunities")
                        
                        similar = rag_system.retrieve_similar_careers(user_description, top_k=3)
                        for i, (career_info, score) in enumerate(similar, 1):
                            with st.expander(f"Opportunity {i} (Match: {score:.0%})"):
                                st.write(career_info)
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please describe your background and interests")

st.markdown("---")
st.markdown("""
### ℹ️ About This RAG System
This application uses **Retrieval-Augmented Generation (RAG)** with Google Gemini AI:
- 🔍 **Retrieval**: Searches knowledge base for relevant careers
- 🧠 **Augmentation**: Provides context to AI model
- ✨ **Generation**: Creates personalized recommendations

**Technology Stack**: Gemini AI + Sentence Transformers + FAISS Vector Store
""")
