"""
Configuration Management Component
Centralizes system configuration and environment variables.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """
    Manages system configuration from environment variables.
    Provides validation and default values.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration from .env file.
        
        Args:
            env_file: Path to .env file (default: .env in current directory)
        """
        if env_file is None:
            env_path = Path(__file__).parent.parent / ".env"
        else:
            env_path = Path(env_file)
        self._base_dir = env_path.parent
        
        # Load environment variables
        load_dotenv(env_path)
        
        # Validate required configuration
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        if not self.get_api_key():
            raise ValueError(
                "HUGGINGFACE_API_KEY not found in environment. "
                "Please set it in .env file or environment variables."
            )
    
    # API Configuration
    def get_api_key(self) -> str:
        """Get HuggingFace API key."""
        return os.getenv("HUGGINGFACE_API_KEY", "")
    
    def get_model_name(self) -> str:
        """Get LLM model name."""
        return os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")
    
    def get_embedding_model(self) -> str:
        """Get embedding model name."""
        return os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Chunking Parameters
    def get_chunk_size(self) -> int:
        """Get document chunk size in characters."""
        return int(os.getenv("CHUNK_SIZE", "1000"))
    
    def get_chunk_overlap(self) -> int:
        """Get overlap size between chunks."""
        return int(os.getenv("CHUNK_OVERLAP", "100"))
    
    # Retrieval Parameters
    def get_top_k(self) -> int:
        """Get number of chunks to retrieve per query."""
        return int(os.getenv("TOP_K", "3"))
    
    # Paths
    def get_data_dir(self) -> Path:
        """Get data directory path."""
        data_dir = Path(os.getenv("DATA_DIR", "./data"))
        if not data_dir.is_absolute():
            data_dir = (self._base_dir / data_dir).resolve()
        data_dir.mkdir(exist_ok=True)
        return data_dir
    
    def get_vector_db_path(self) -> Path:
        """Get vector database path."""
        db_path = Path(os.getenv("VECTOR_DB_PATH", "./chroma_db"))
        if not db_path.is_absolute():
            db_path = (self._base_dir / db_path).resolve()
        return db_path
    
    def __repr__(self) -> str:
        """String representation (masks API key)."""
        masked_key = self.get_api_key()[:8] + "..." if self.get_api_key() else "None"
        return (
            f"Config(model={self.get_model_name()}, "
            f"embedding={self.get_embedding_model()}, "
            f"chunk_size={self.get_chunk_size()}, "
            f"api_key={masked_key})"
        )
