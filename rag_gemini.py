"""
Enhanced RAG Pipeline using Google Gemini AI and ChromaDB vector store.
Reads knowledge base from TXT files, implements text chunking, creates embeddings, and stores in vector database.
"""

import os
from typing import List, Tuple
from groq import Groq
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


class CareerRAG:
    """Enhanced RAG system for career recommendations using Gemini AI with FAISS vector database"""

    def __init__(self, knowledge_base_path: str = "data"):
        """
        Initialize RAG with FAISS vector store (no API key needed for retrieval).

        Args:
            knowledge_base_path: Path to the knowledge base directory containing TXT files
        """
        self.knowledge_base_path = knowledge_base_path

        # Initialize embeddings and vector store (retrieval components)
        self.embeddings_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.vector_store = None
        self.documents = None






    def load_documents(self) -> List[Document]:
        """
        Load documents from TXT files in data directory.

        Returns:
            List of Document objects containing raw text sections
        """
        documents = []

        # Check if knowledge_base_path is a directory
        if os.path.isdir(self.knowledge_base_path):
            # Read all .txt files from the directory
            txt_files = [f for f in os.listdir(self.knowledge_base_path) if f.endswith('.txt')]
            if not txt_files:
                raise FileNotFoundError(f"No .txt files found in directory: {self.knowledge_base_path}")

            print(f"📂 Found {len(txt_files)} knowledge base files: {', '.join(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(self.knowledge_base_path, txt_file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()

                    # Split content into sections (separated by ---)
                    sections = [section.strip() for section in content.split('---') if section.strip()]

                    # Create Document objects with file-specific metadata
                    file_documents = [Document(page_content=section,
                                             metadata={"source": txt_file, "section": i})
                                    for i, section in enumerate(sections)]
                    documents.extend(file_documents)

                    print(f"📄 Loaded {len(sections)} sections from {txt_file}")

                except FileNotFoundError:
                    print(f"⚠️ Warning: File not found: {file_path}")
                    continue
                except Exception as e:
                    print(f"⚠️ Warning: Error reading {file_path}: {e}")
                    continue

        else:
            # Fallback to single file reading for backward compatibility
            try:
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"Knowledge base file not found: {self.knowledge_base_path}")

            # Split content into sections (separated by ---)
            sections = [section.strip() for section in content.split('---') if section.strip()]

            # Create Document objects
            documents = [Document(page_content=section, metadata={"source": self.knowledge_base_path, "section": i})
                        for i, section in enumerate(sections)]

            print(f"📄 Loaded {len(sections)} sections from {self.knowledge_base_path}")

        if not documents:
            raise ValueError("No documents loaded from knowledge base")

        return documents


    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval.

        Args:
            documents: List of Document objects to chunk

        Returns:
            List of chunked Document objects
        """
        # Initialize text splitter for chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Maximum characters per chunk
            chunk_overlap=200,  # Overlap between chunks
            separators=["\n\n", "\n", ". ", " ", ""]  # Split on paragraphs, lines, sentences, words
        )

        # Split documents into chunks
        chunked_documents = text_splitter.split_documents(documents)

        print(f"✂️ Split into {len(chunked_documents)} chunks from {len(documents)} sections")

        return chunked_documents


    def load_knowledge_base(self) -> List[Document]:
        """
        Load and chunk the knowledge base from TXT files in data directory.
        This method combines document loading and chunking for backward compatibility.

        Returns:
            List of Document objects containing chunked text
        """
        documents = self.load_documents()
        chunked_documents = self.chunk_documents(documents)
        return chunked_documents
    




    def create_vector_store(self) -> None:
        """
        Create ChromaDB vector store from knowledge base documents with explicit pipeline steps.
        """
        print("📚 Step 1: Loading documents...")
        raw_documents = self.load_documents()

        print("✂️ Step 2: Chunking documents...")
        self.documents = self.chunk_documents(raw_documents)

        print("🔍 Step 3: Creating embeddings and storing in ChromaDB vector database...")
        # Create ChromaDB vector store with explicit pipeline
        self.vector_store = Chroma.from_documents(
            documents=self.documents,
            embedding=self.embeddings_model,
            collection_name="career_knowledge_base",
            persist_directory="./chroma_db"
        )

        print("✅ Vector store created successfully")




    def retrieve_similar_documents(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """
        Retrieve similar documents using semantic similarity.

        Args:
            query: User input (skills, interests, description)
            top_k: Number of results to return

        Returns:
            List of (Document, similarity_score) tuples
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized. Call create_vector_store first.")

        # Perform similarity search
        docs_and_scores = self.vector_store.similarity_search_with_score(query, k=top_k)

        return docs_and_scores
    







    def recommend_career(self, user_query: str, api_key: str = None) -> Tuple[str, float]:
        """
        Generate career recommendation using RAG pipeline:
        1. User query → Retriever → Vector Store
        2. Retrieved context + prompt → LLM → Output

        Args:
            user_query: User profile (skills, interests, experience)
            api_key: Google Gemini API key (required for LLM generation)

        Returns:
            Tuple of (recommendation, confidence_score)
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized. Call create_vector_store first.")

        # Step 1: User query goes into retriever connected to vector store
        print("🔍 Step 1: Retrieving relevant career information...")
        retrieved_docs = self.retrieve_similar_documents(user_query, top_k=3)

        # Extract context from retrieved documents
        context = "\n\n".join([doc.page_content for doc, score in retrieved_docs])
        sources = [doc.metadata.get('source', 'unknown') for doc, score in retrieved_docs]

        print(f"📄 Retrieved {len(retrieved_docs)} relevant career paths from: {set(sources)}")

        # Step 2: Get API key for LLM (only needed at this final step)
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("API key required for LLM generation. Pass api_key parameter or set GROQ_API_KEY environment variable.")

        # Step 3: Initialize LLM with API key (step-wise integration)
        print("🔑 Step 3: Initializing LLM for final generation...")
        client = Groq(api_key=api_key)
        model_name = 'llama-3.1-70b-versatile'
        # Model is specified in generate_content call

        # Step 4: LLM gets context + prompt (what user needs to fetch)
        print("🤖 Step 4: Generating personalized recommendation...")

        prompt = f"""You are an expert career counselor with access to a comprehensive database of career paths.

USER QUERY: {user_query}

RETRIEVED CAREER CONTEXT:
{context}

TASK: Based on the user's query and the retrieved career information above, provide a personalized career recommendation that includes:

1. **Top Career Recommendations**: Suggest 2-3 most suitable careers with specific reasons why they match
2. **Skills Match Analysis**: What skills they already have vs. what they need to develop
3. **Career Path Details**: Salary ranges, experience levels, growth opportunities
4. **Action Plan**: Specific next steps, learning resources, and timeline
5. **Alternative Options**: Other career paths they might consider

Be specific, encouraging, and provide actionable advice. Focus on careers that align with their stated interests and skills."""

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            recommendation = response.choices[0].message.content

            # Step 5: Calculate confidence based on retrieval scores
            confidence = sum(score for _, score in retrieved_docs) / len(retrieved_docs) if retrieved_docs else 0.5

            print("✅ Step 5: Recommendation generated successfully")
            return recommendation, confidence

        except Exception as e:
            error_msg = f"Error in LLM generation: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg, 0.0
        





    def save_vector_store(self, path: str = "./chroma_db") -> None:
        """
        Save the ChromaDB vector store to disk.
        Note: ChromaDB automatically persists when created with persist_directory.

        Args:
            path: Directory path (not used for ChromaDB as it auto-persists)
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized. Call create_vector_store first.")

        # ChromaDB persists automatically, but we can force persist if needed
        try:
            self.vector_store.persist()
            print(f"💾 Vector store persisted to {path}")
        except AttributeError:
            # persist() method might not exist in all versions
            print("💾 Vector store is automatically persisted with ChromaDB")






    def load_vector_store(self, path: str = "./chroma_db") -> None:
        """
        Load the ChromaDB vector store from disk.

        Args:
            path: Directory path to load the vector store from
        """
        try:
            self.vector_store = Chroma(
                collection_name="career_knowledge_base",
                embedding_function=self.embeddings_model,
                persist_directory=path
            )
            print(f"📂 Vector store loaded from {path}")
        except Exception as e:
            print(f"❌ Failed to load vector store: {e}")
            print("Creating new vector store...")
            self.create_vector_store()



