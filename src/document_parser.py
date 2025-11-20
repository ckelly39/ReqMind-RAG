"""
Document Parser Component
Extracts text from PDF files using LangChain's PyPDFLoader.
"""

from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class DocumentParser:
    """
    Parses PDF documents and converts them into Document objects.
    Uses LangChain's PyPDFLoader for reliable PDF text extraction.
    """
    
    def parse_pdf(self, file_path: Path) -> List[Document]:
        """
        Parse a single PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of Document objects (one per page)
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If file is not a PDF
        """
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if file_path.suffix.lower() != '.pdf':
            raise ValueError(f"File must be a PDF: {file_path}")
        
        # Use LangChain's PyPDFLoader
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        
        print(f"✓ Parsed {len(documents)} pages from {file_path.name}")
        return documents
    
    def parse_directory(self, directory: Path) -> List[Document]:
        """
        Parse all PDF files in a directory.
        
        Args:
            directory: Path to directory containing PDFs
            
        Returns:
            List of all Document objects from all PDFs
        """
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        pdf_files = list(directory.glob("*.pdf"))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {directory}")
        
        print(f"\nFound {len(pdf_files)} PDF file(s)")
        
        all_documents = []
        for pdf_file in pdf_files:
            documents = self.parse_pdf(pdf_file)
            all_documents.extend(documents)
        
        print(f"✓ Total: {len(all_documents)} pages extracted\n")
        return all_documents
    
    def get_metadata(self, doc: Document) -> dict:
        """
        Extract metadata from a Document object.
        
        Args:
            doc: Document object
            
        Returns:
            Dictionary of metadata
        """
        return doc.metadata
