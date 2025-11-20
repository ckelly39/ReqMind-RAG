"""
ReqMind - Requirements Document Q&A System
A RAG (Retrieval-Augmented Generation) system for querying software requirements documents.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .config import Config
from .document_parser import DocumentParser
from .text_splitter import TextSplitter
from .embedding_generator import EmbeddingGenerator
from .vector_store import VectorStore
from .retrieval_component import RetrievalComponent
from .inference_client import InferenceClient
from .llm import HuggingFaceInferenceLLM
from .retrieval_qa import RetrievalQAComponent
from .client_ui import ClientUI

__all__ = [
    "Config",
    "DocumentParser",
    "TextSplitter",
    "EmbeddingGenerator",
    "VectorStore",
    "RetrievalComponent",
    "InferenceClient",
    "HuggingFaceInferenceLLM",
    "RetrievalQAComponent",
    "ClientUI"
]
