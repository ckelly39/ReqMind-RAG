"""Document ingestion module for loading and processing requirements documents."""

from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config


class DocumentIngester:
    """Handles loading and chunking of requirements documents."""
    
    def __init__(self, chunk_size: int = config.CHUNK_SIZE, 
                 chunk_overlap: int = config.CHUNK_OVERLAP):
        """Initialize the document ingester.
        
        Args:
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between consecutive chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_documents(self, documents_dir: Path) -> List[Document]:
        """Load all text documents from the specified directory.
        
        Args:
            documents_dir: Path to directory containing documents
            
        Returns:
            List of Document objects
        """
        documents = []
        
        if not documents_dir.exists():
            documents_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created documents directory at {documents_dir}")
            return documents
        
        # Load .txt files
        for file_path in documents_dir.glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={"source": str(file_path.name)}
                )
                documents.append(doc)
        
        print(f"Loaded {len(documents)} documents from {documents_dir}")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of chunked documents
        """
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def process_documents(self, documents_dir: Path) -> List[Document]:
        """Load and split documents in one step.
        
        Args:
            documents_dir: Path to directory containing documents
            
        Returns:
            List of processed document chunks
        """
        documents = self.load_documents(documents_dir)
        if not documents:
            return []
        return self.split_documents(documents)
