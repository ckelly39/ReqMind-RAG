"""
Retrieval Component
Provides high-level interface for document retrieval.
Wraps VectorStore's retriever functionality with additional features.
"""

from typing import List, Optional
from langchain_core.documents import Document


class RetrievalComponent:
    """
    Manages document retrieval from the vector store.
    Provides clean interface for text-based and embedding-based retrieval.
    """
    
    def __init__(self, vector_store, top_k: int = 3):
        """
        Initialize retrieval component.
        
        Args:
            vector_store: VectorStore instance
            top_k: Number of documents to retrieve by default
        """
        self.vector_store = vector_store
        self.top_k = top_k
        
        # Get retriever from vector store
        self.retriever = vector_store.as_retriever(k=top_k)
        
        print(f"✓ RetrievalComponent initialized (top_k={top_k})\n")
    
    def retrieve_by_text(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """
        Retrieve documents by text query.
        
        Args:
            query: Query text
            top_k: Number of results (overrides default if provided)
            
        Returns:
            List of most similar Document objects
        """
        k = top_k if top_k is not None else self.top_k
        
        # Use vector store's query method
        results = self.vector_store.query(query, k=k)
        
        return results
    
    def get_retriever(self):
        """
        Get LangChain retriever object.
        Used by RetrievalQA chain.
        
        Returns:
            LangChain retriever
        """
        return self.retriever
    
    def set_top_k(self, k: int) -> None:
        """
        Update the number of documents to retrieve.
        
        Args:
            k: New top_k value
        """
        self.top_k = k
        self.retriever = self.vector_store.as_retriever(k=k)
        print(f"✓ Updated top_k to {k}")
