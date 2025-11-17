"""
RAG Pipeline using Google Gemini AI and FAISS vector store.
Simpler, faster, and avoids LangChain import issues.
"""

import os
import json
from typing import List, Tuple
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np

# Load environment variables from .env file
load_dotenv()


class CareerRAG:
    """RAG system for career recommendations using Gemini AI"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize RAG with Gemini API.
        
        Args:
            api_key: Google Gemini API key (uses GEMINI_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set environment variable or pass api_key.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Use sentence-transformers for embeddings (no API calls needed)
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.career_embeddings = None
        self.career_documents = None
    
    def create_knowledge_base(self, documents: List[str]) -> None:
        """
        Create vector store from career documents.
        
        Args:
            documents: List of career document strings
        """
        self.career_documents = documents
        
        # Generate embeddings for all documents
        print(f"📊 Generating embeddings for {len(documents)} careers...")
        self.career_embeddings = self.embeddings_model.encode(documents, convert_to_tensor=True)
        print("✅ Embeddings generated successfully")
    
    def retrieve_similar_careers(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Retrieve similar careers using semantic similarity.
        
        Args:
            query: User input (skills, interests, description)
            top_k: Number of results to return
            
        Returns:
            List of (career_info, similarity_score) tuples
        """
        if self.career_embeddings is None:
            raise RuntimeError("Knowledge base not initialized. Call create_knowledge_base first.")
        
        # Encode query
        query_embedding = self.embeddings_model.encode(query, convert_to_tensor=True)
        
        # Compute similarities
        from sentence_transformers import util
        similarities = util.pytorch_cos_sim(query_embedding, self.career_embeddings)[0]
        
        # Get top-k results
        top_results = np.argsort(-similarities.cpu().numpy())[:top_k]
        
        results = []
        for idx in top_results:
            score = float(similarities[idx].cpu().numpy())
            results.append((self.career_documents[idx], score))
        
        return results
    
    def recommend_career(self, user_input: str) -> Tuple[str, float]:
        """
        Generate career recommendation using Gemini AI.
        
        Args:
            user_input: User profile (skills, interests, experience)
            
        Returns:
            Tuple of (recommendation, confidence_score)
        """
        if self.career_embeddings is None:
            raise RuntimeError("Knowledge base not initialized.")
        
        # Retrieve relevant careers
        similar_careers = self.retrieve_similar_careers(user_input, top_k=3)
        context = "\n\n".join([career[0] for career in similar_careers])
        
        # Build prompt for Gemini
        prompt = f"""You are an expert career counselor. Based on the user's profile and relevant career information, provide personalized recommendations.

USER PROFILE:
{user_input}

RELEVANT CAREER INFORMATION:
{context}

Please provide:
1. Top recommended career(s) with specific reasons
2. Why this career matches their profile
3. Skills they already possess
4. Skills to develop
5. Learning resources and next steps

Be encouraging, specific, and actionable."""
        
        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)
            recommendation = response.text
            
            # Use highest similarity score as confidence
            confidence = similar_careers[0][1] if similar_careers else 0.5
            
            return recommendation, confidence
        
        except Exception as e:
            return f"Error generating recommendation: {str(e)}", 0.0


def demo_rag():
    """Demo function to test RAG with sample careers"""
    from career_knowledge_base import get_career_documents
    
    print("🚀 Initializing Gemini RAG Pipeline...")
    rag = CareerRAG()
    
    print("📚 Loading career knowledge base...")
    docs = get_career_documents()
    rag.create_knowledge_base(docs)
    
    print("\n" + "="*60)
    print("🎯 Testing Career Recommendation")
    print("="*60)
    
    # Test case
    test_input = "I have 2 years of Python experience, love machine learning and data analysis, want to build scalable systems"
    
    print(f"\nUser Profile: {test_input}\n")
    print("Generating recommendation...")
    
    recommendation, confidence = rag.recommend_career(test_input)
    print(f"\n✅ Confidence Score: {confidence:.0%}")
    print(f"\n📝 Recommendation:\n{recommendation}")
    
    print("\n" + "="*60)
    print("Similar Careers:")
    print("="*60)
    
    similar = rag.retrieve_similar_careers(test_input, top_k=3)
    for i, (career, score) in enumerate(similar, 1):
        print(f"\n{i}. Similarity: {score:.0%}")
        print(career[:200] + "...")


if __name__ == "__main__":
    demo_rag()
