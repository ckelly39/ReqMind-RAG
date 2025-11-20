"""
Vector Store Component (Singleton Pattern)
Manages persistent vector storage using ChromaDB.
Implements Singleton pattern to ensure single instance and prevent resource conflicts.
"""

from pathlib import Path
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


class VectorStore:
    """
    Singleton Vector Store managing ChromaDB for persistent vector storage.
    Ensures only one instance exists to optimize memory and prevent conflicts.
    """
    
    _instance: Optional['VectorStore'] = None
    _initialized: bool = False
    
    def __new__(cls, *args, **kwargs):
        """
        Singleton pattern implementation.
        Ensures only one instance of VectorStore exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self, 
        embeddings: HuggingFaceEmbeddings,
        persist_directory: Path,
        collection_name: str = "reqmind_collection"
    ):
        """
        Initialize Vector Store with ChromaDB.
        Note: Due to Singleton, only first initialization parameters are used.
        
        Args:
            embeddings: Embedding generator instance
            persist_directory: Path to persist ChromaDB data
            collection_name: Name of the collection
        """
        # Only initialize once (Singleton pattern)
        if VectorStore._initialized:
            return
        
        self.embeddings = embeddings
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.vector_store: Optional[Chroma] = None
        
        VectorStore._initialized = True
        print(f"✓ VectorStore singleton instance created")
        print(f"  Location: {persist_directory}")
        print(f"  Collection: {collection_name}\n")
    
    def create_from_documents(self, documents: List[Document]) -> None:
        """
        Create vector store from documents.
        Generates embeddings and stores them in ChromaDB.
        
        Args:
            documents: List of Document objects (chunks) to embed and store
        """
        print(f"Creating vector store from {len(documents)} documents...")
        
        # More robust validation and cleaning of documents
        valid_documents = []
        texts = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            # Check if document has valid content
            if not hasattr(doc, 'page_content'):
                continue
            
            content = doc.page_content
            
            # Skip if content is not a string or is empty/whitespace
            if not isinstance(content, str):
                print(f"⚠️  Skipping document {i}: not a string (type: {type(content)})")
                continue
            
            # Clean and validate the content
            cleaned_content = content.strip()
            if not cleaned_content:
                print(f"⚠️  Skipping document {i}: empty after stripping")
                continue
            
            # Replace any null bytes or other problematic characters
            cleaned_content = cleaned_content.replace('\x00', '').replace('\r', ' ')
            
            # Final check - ensure it's a valid string
            if len(cleaned_content) < 10:  # Skip very short chunks
                print(f"⚠️  Skipping document {i}: too short ({len(cleaned_content)} chars)")
                continue
            
            # Add to valid lists
            texts.append(cleaned_content)
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            metadatas.append(metadata)
            
            # Create document for the list
            cleaned_doc = Document(
                page_content=cleaned_content,
                metadata=metadata
            )
            valid_documents.append(cleaned_doc)
        
        filtered_count = len(documents) - len(valid_documents)
        if filtered_count > 0:
            print(f"⚠️  Filtered out {filtered_count} invalid/empty chunks")
        
        print(f"Processing {len(valid_documents)} valid chunks...")
        
        # Initialize empty Chroma store first
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=str(self.persist_directory),
            collection_name=self.collection_name
        )
        
        # Add texts in smaller batches to avoid issues
        batch_size = 10
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            
            try:
                self.vector_store.add_texts(
                    texts=batch_texts,
                    metadatas=batch_metadatas
                )
                print(f"  Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            except Exception as e:
                print(f"⚠️  Error in batch {i//batch_size + 1}, trying individually...")
                # If batch fails, try one by one
                for j, (text, metadata) in enumerate(zip(batch_texts, batch_metadatas)):
                    try:
                        self.vector_store.add_texts(
                            texts=[text],
                            metadatas=[metadata]
                        )
                    except Exception as e2:
                        print(f"⚠️  Failed to add document {i+j}: {str(e2)[:100]}")
        
        print(f"✓ Vector store created with {len(valid_documents)} chunks")
        print("Vector store ready for retrieval\n")
    
    def load_existing(self) -> bool:
        """
        Load existing vector store from disk.
        
        Returns:
            True if successfully loaded, False if no existing store found
        """
        if not self.persist_directory.exists():
            return False
        
        try:
            print(f"Loading existing vector store from {self.persist_directory}...")
            
            self.vector_store = Chroma(
                persist_directory=str(self.persist_directory),
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            
            # Check if store has data
            collection = self.vector_store._collection
            count = collection.count()
            
            if count == 0:
                print("  Vector store exists but is empty")
                return False
            
            print(f"✓ Loaded existing vector store with {count} chunks\n")
            return True
            
        except Exception as e:
            print(f"  Could not load existing store: {e}")
            return False
    
    def query(self, query_text: str, k: int = 3) -> List[Document]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: Query string
            k: Number of results to return
            
        Returns:
            List of most similar Document objects
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Call create_from_documents or load_existing first.")
        
        # Use LangChain's similarity_search
        results = self.vector_store.similarity_search(query_text, k=k)
        return results
    
    def as_retriever(self, k: int = 3):
        """
        Get retriever interface for the vector store.
        Used by RetrievalQA chain.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            LangChain retriever object
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized.")
        
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )
    
    def persist(self) -> None:
        """
        Persist the vector store to disk.
        Note: Modern Chroma versions auto-persist when persist_directory is set.
        """
        if self.vector_store is not None:
            # Newer versions of Chroma auto-persist, so we just confirm
            print(f"✓ Vector store auto-persisted to {self.persist_directory}")
    
    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset singleton instance (mainly for testing).
        Warning: Use with caution in production.
        """
        cls._instance = None
        cls._initialized = False
