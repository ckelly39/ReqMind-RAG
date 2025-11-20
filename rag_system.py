"""RAG query system for answering questions about requirements."""

from typing import Optional
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
        
        # Initialize retriever
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": config.TOP_K_RESULTS}
        )
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        
        print("RAG system initialized")
    
    def _initialize_llm(self):
        """Initialize the language model.
        
        Returns:
            Language model instance
        """
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
        
        return llm
    
    def _format_context(self, documents):
        """Format retrieved documents into context.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Unknown')
            context_parts.append(f"[{i}] From {source}:\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Create a prompt for the LLM.
        
        Args:
            question: User's question
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        prompt = f"""Answer the question based on the context below. If the answer cannot be found in the context, say "I cannot find that information in the provided documents."

Context:
{context}

Question: {question}

Answer:"""
        return prompt
    
    def query(self, question: str) -> dict:
        """Query the RAG system with a natural language question.
        
        Args:
            question: Natural language question about requirements
            
        Returns:
            Dictionary with 'result' and 'source_documents'
        """
        print(f"\nProcessing query: {question}")
        
        # Retrieve relevant documents
        source_documents = self.retriever.invoke(question)
        
        # Format context
        context = self._format_context(source_documents)
        
        # Create prompt
        prompt = self._create_prompt(question, context)
        
        # Generate answer
        answer = self.llm.invoke(prompt)
        
        return {
            "result": answer,
            "source_documents": source_documents
        }
    
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
