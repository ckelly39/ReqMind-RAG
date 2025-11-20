A Retrieval-Augmented Generation (RAG) system for querying software requirements documents using natural language.

📖 Overview
ReqMind helps software engineers quickly find information in large requirements documents by combining semantic search with AI-powered answer generation. Simply ask questions in natural language and get accurate answers with source citations.
✨ Key Highlights

🔍 Natural Language Queries - Ask questions like "What are the authentication requirements?"
🔒 Privacy-Focused - Local embeddings, no data sent to external services
💰 Cost-Effective - Free local embeddings, pay only for LLM inference
📚 Source Citations - Every answer includes document sources and page numbers
⚡ Fast - Persistent vector storage for instant subsequent queries
🎨 Clean Architecture - Two-pipeline design with proper design patterns


🚀 Features
Core Functionality

✅ PDF document processing and chunking
✅ Semantic vector embeddings (local, 384-dimensional)
✅ Persistent ChromaDB vector storage
✅ Natural language question answering
✅ Source attribution with page numbers
✅ Conversation history tracking
✅ Interactive command-line interface

Technical Features

✅ Two-Pipeline Architecture: Offline loading + runtime inference
✅ Design Patterns: Singleton (VectorStore), Adapter (InferenceClient)
✅ LangChain Integration: PyPDFLoader, RecursiveTextSplitter, Chroma, RetrievalQA
✅ Modern Python: Type hints, error handling, comprehensive logging
✅ Configurable: Environment-based configuration management
