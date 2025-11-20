"""Vector store module for ChromaDB integration."""

from pathlib import Path
from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import config


class VectorStoreManager:
    """Manages ChromaDB vector store for document embeddings."""
    
    def __init__(self, 
                 persist_directory: Path = config.CHROMA_DB_DIR,
                 embedding_model: str = config.EMBEDDING_MODEL,
                 collection_name: str = config.COLLECTION_NAME):
        """Initialize the vector store manager.
        
        Args:
            persist_directory: Directory to persist the vector store
            embedding_model: HuggingFace model for embeddings
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize embeddings
        print(f"Loading embedding model: {embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        
        self.vector_store = None
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create a new vector store from documents.
        
        Args:
            documents: List of documents to embed
            
        Returns:
            ChromaDB vector store
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        print(f"Creating vector store with {len(documents)} documents...")
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=str(self.persist_directory)
        )
        print("Vector store created successfully")
        return self.vector_store
    
    def load_vector_store(self) -> Optional[Chroma]:
        """Load an existing vector store from disk.
        
        Returns:
            ChromaDB vector store if exists, None otherwise
        """
        if not self.persist_directory.exists():
            print("No existing vector store found")
            return None
        
        try:
            print("Loading existing vector store...")
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            print("Vector store loaded successfully")
            return self.vector_store
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return None
    
    def get_or_create_vector_store(self, documents: Optional[List[Document]] = None) -> Chroma:
        """Get existing vector store or create new one.
        
        Args:
            documents: Documents to use if creating new store
            
        Returns:
            ChromaDB vector store
        """
        vector_store = self.load_vector_store()
        
        if vector_store is None:
            if documents is None or len(documents) == 0:
                raise ValueError("No documents provided and no existing vector store found")
            vector_store = self.create_vector_store(documents)
        
        return vector_store
    
    def add_documents(self, documents: List[Document]):
        """Add documents to existing vector store.
        
        Args:
            documents: Documents to add
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        print(f"Adding {len(documents)} documents to vector store...")
        self.vector_store.add_documents(documents)
        print("Documents added successfully")
    
    def similarity_search(self, query: str, k: int = config.TOP_K_RESULTS) -> List[Document]:
        """Search for similar documents.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.similarity_search(query, k=k)
