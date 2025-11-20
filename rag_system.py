"""RAG query system for answering questions about requirements."""

from typing import Optional
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
import config


class RAGQuerySystem:
    """Handles question-answering using RAG approach."""
    
    def __init__(self, vector_store, use_local_llm: bool = True):
        """Initialize the RAG query system.
        
        Args:
            vector_store: ChromaDB vector store instance
            use_local_llm: Whether to use local LLM (True) or HuggingFace API (False)
        """
        self.vector_store = vector_store
        self.use_local_llm = use_local_llm
        self.qa_chain = None
        
        # Initialize retriever
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": config.TOP_K_RESULTS}
        )
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        
        # Create QA chain
        self._create_qa_chain()
    
    def _initialize_llm(self):
        """Initialize the language model.
        
        Returns:
            Language model instance
        """
        if self.use_local_llm:
            print("Initializing local LLM pipeline...")
            # Use a small, fast model for question answering
            qa_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-small",
                max_length=512,
                device=-1  # CPU
            )
            llm = HuggingFacePipeline(pipeline=qa_pipeline)
            print("Local LLM initialized")
        else:
            # This would require HUGGINGFACEHUB_API_TOKEN environment variable
            print("Initializing HuggingFace Hub LLM...")
            llm = HuggingFaceHub(
                repo_id="google/flan-t5-base",
                model_kwargs={"temperature": 0.7, "max_length": 512}
            )
            print("HuggingFace Hub LLM initialized")
        
        return llm
    
    def _create_qa_chain(self):
        """Create the RetrievalQA chain."""
        print("Creating QA chain...")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            verbose=False
        )
        print("QA chain created")
    
    def query(self, question: str) -> dict:
        """Query the RAG system with a natural language question.
        
        Args:
            question: Natural language question about requirements
            
        Returns:
            Dictionary with 'result' and 'source_documents'
        """
        if self.qa_chain is None:
            raise ValueError("QA chain not initialized")
        
        print(f"\nProcessing query: {question}")
        response = self.qa_chain.invoke({"query": question})
        
        return response
    
    def query_with_context(self, question: str) -> dict:
        """Query and return formatted response with source context.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary with answer and sources
        """
        response = self.query(question)
        
        # Format response
        formatted_response = {
            "answer": response["result"],
            "sources": []
        }
        
        # Extract source information
        for doc in response.get("source_documents", []):
            source_info = {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            formatted_response["sources"].append(source_info)
        
        return formatted_response
