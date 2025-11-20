"""Configuration settings for ReqMind-RAG system."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Document storage
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ChromaDB settings
COLLECTION_NAME = "requirements_docs"

# Chunk settings for document processing
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Query settings
TOP_K_RESULTS = 3
