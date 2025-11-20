"""
Text Splitter Component
Splits documents into smaller chunks using LangChain's text splitters.
Implements Strategy pattern for different splitting approaches.
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class TextSplitter:
    """
    Splits documents into chunks for optimal embedding and retrieval.
    Uses LangChain's RecursiveCharacterTextSplitter for intelligent splitting.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initialize text splitter with chunking parameters.
        
        Args:
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Create LangChain's RecursiveCharacterTextSplitter
        # This intelligently splits by paragraphs, then sentences, then characters
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split a list of documents into chunks.
        
        Args:
            documents: List of Document objects to split
            
        Returns:
            List of Document objects (chunks) with preserved metadata
        """
        # Use LangChain's split_documents method
        # This preserves metadata and handles the chunking logic
        chunks = self.splitter.split_documents(documents)
        
        print(f"✓ Split {len(documents)} documents into {len(chunks)} chunks")
        print(f"  Chunk size: {self.chunk_size} chars, Overlap: {self.chunk_overlap} chars")
        
        # Print first 500 characters of first chunk (Task 2b)
        if chunks:
            first_chunk_preview = chunks[0].page_content[:500]
            print(f"\nFirst chunk preview (first 500 characters):")
            print(f"{first_chunk_preview}\n")
        
        return chunks
    
    def get_chunk_stats(self, chunks: List[Document]) -> dict:
        """
        Get statistics about the chunks.
        
        Args:
            chunks: List of Document chunks
            
        Returns:
            Dictionary with chunk statistics
        """
        chunk_lengths = [len(chunk.page_content) for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "avg_chunk_length": sum(chunk_lengths) / len(chunks) if chunks else 0,
            "min_chunk_length": min(chunk_lengths) if chunks else 0,
            "max_chunk_length": max(chunk_lengths) if chunks else 0
        }
