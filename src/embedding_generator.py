"""
Embedding Generator Component
Generates vector embeddings using local SentenceTransformer models.
Uses LangChain's HuggingFaceEmbeddings for integration.
"""

from typing import List
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingGenerator:
    """
    Generates embeddings for text chunks using local SentenceTransformer models.
    Runs offline without API calls, ensuring privacy and predictable costs.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator with specified model.
        
        Args:
            model_name: Name of SentenceTransformer model to use
                       Default: all-MiniLM-L6-v2 (384 dimensions, fast, good quality)
        """
        self.model_name = model_name
        
        print(f"Loading embedding model: {model_name}...")
        
        # Use LangChain's HuggingFaceEmbeddings wrapper
        # This handles model loading and embedding generation
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},  # Use CPU (change to 'cuda' for GPU)
            encode_kwargs={'normalize_embeddings': True}  # L2 normalization
        )
        
        print(f"✓ Embedding model loaded: {model_name}\n")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each is a list of floats)
        """
        embeddings = self.embeddings.embed_documents(texts)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector (list of floats)
        """
        embedding = self.embeddings.embed_query(text)
        return embedding
    
    def get_dimension(self) -> int:
        """
        Get the dimensionality of embeddings.
        
        Returns:
            Number of dimensions (384 for all-MiniLM-L6-v2)
        """
        # Generate a test embedding to get dimension
        test_embedding = self.embed_query("test")
        return len(test_embedding)
    
    def get_model_name(self) -> str:
        """Get the name of the embedding model."""
        return self.model_name
