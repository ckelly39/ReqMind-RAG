# ReqMind - Requirements Document Q&A System

A Retrieval-Augmented Generation (RAG) system for querying software requirements documents using natural language. Built with LangChain, ChromaDB, and HuggingFace.

## 🎯 Overview

ReqMind helps software engineers quickly find information in large requirements documents by:
- Loading and processing PDF requirements documents
- Creating semantic embeddings for intelligent search
- Answering natural language questions with relevant citations
- Using local embeddings (privacy-focused, no API costs)
- Leveraging HuggingFace's Mistral 7B for answer generation

## 🏗️ Architecture

The system implements a **two-pipeline architecture**:

### Loading Pipeline (Offline)
Runs once to prepare documents for searching:
1. **Document Parser** - Extracts text from PDFs (LangChain PyPDFLoader)
2. **Text Splitter** - Splits into 1000-char chunks (LangChain RecursiveCharacterTextSplitter)
3. **Embedding Generator** - Creates 384-dim vectors (SentenceTransformer local)
4. **Vector Store** - Stores in ChromaDB (Singleton pattern)

### Inference Pipeline (Runtime)
Handles user queries in real-time:
1. **Retrieval Component** - Searches for relevant chunks
2. **RetrievalQA** - Orchestrates RAG workflow (LangChain chain)
3. **Custom LLM** - Generates answers (HuggingFace Inference API)
4. **Client UI** - Interactive command-line interface

## 🎨 Design Patterns

### 1. Singleton Pattern
**Where:** Vector Store component
**Why:** Ensures single ChromaDB instance, prevents resource conflicts, optimizes memory

### 2. Adapter Pattern  
**Where:** InferenceClient component
**Why:** Wraps HuggingFace API, isolates system from external API changes, enables easy provider switching

## 📋 Prerequisites

- Python 3.8+
- HuggingFace API key (free tier available)
- 4GB+ RAM (for local embeddings)
- PDF requirements documents

## 🚀 Installation

### 1. Clone/Download the Project
```bash
cd reqmind
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your HuggingFace API key
HUGGINGFACE_API_KEY=your_key_here
```

**Get HuggingFace API Key:**
1. Go to https://huggingface.co/settings/tokens
2. Create new token (read access sufficient)
3. Copy to .env file

### 5. Add PDF Documents
```bash
# Create data directory
mkdir -p data

# Add your PDF files
cp /path/to/RequirementsDocument.pdf data/
```

## 💻 Usage

### Basic Usage
```bash
cd src
python main.py
```

The system will:
1. Load and process your PDFs (first run only)
2. Create vector database (cached for future runs)
3. Start interactive Q&A session

### Example Session
```
🤖 ReqMind - Requirements Document Q&A System
======================================================================

Welcome! I can help you search through requirements documents.

Example questions you can ask:
  • What are the authentication requirements?
  • What is the maximum response time?
  • Tell me about the security requirements?

Commands:
  • 'exit' or 'quit' - Exit the system
  • 'history' - Show conversation history

----------------------------------------------------------------------

💬 Your question: What are the authentication requirements?

🔍 Searching documents...

📝 Answer:
----------------------------------------------------------------------
The system implements multi-factor authentication (MFA) for 
administrative accounts. It enforces strong password policies including
minimum length, complexity requirements, and regular password changes.
The system also implements role-based access control (RBAC) to restrict
access based on user roles...

📚 Sources:
----------------------------------------------------------------------
1. Source: RequirementsDocument.pdf, Page: 15
   Snippet: NFR-22: The system SHALL implement multi-factor authentication...

2. Source: RequirementsDocument.pdf, Page: 16
   Snippet: NFR-24: The system SHALL implement role-based access control...

----------------------------------------------------------------------
```

### Commands
- **Regular question** - Ask anything about your documents
- **`history`** - View conversation history
- **`clear`** - Clear conversation history
- **`exit`** or **`quit`** - Exit the system

## 📁 Project Structure

```
reqmind/
├── .env.example              # Configuration template
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/                     # Your PDF files
│   └── RequirementsDocument.pdf
├── chroma_db/               # Vector database (auto-created)
└── src/
    ├── __init__.py
    ├── main.py              # Entry point
    ├── config.py            # Configuration management
    ├── document_parser.py   # PDF loading (LangChain)
    ├── text_splitter.py     # Text chunking (LangChain)
    ├── embedding_generator.py  # Local embeddings
    ├── vector_store.py      # ChromaDB (Singleton)
    ├── retrieval_component.py  # Retrieval interface
    ├── inference_client.py  # API adapter (Adapter pattern)
    ├── llm.py              # Custom LangChain LLM
    ├── retrieval_qa.py     # RAG orchestrator
    └── client_ui.py        # Command-line UI
```

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# HuggingFace Configuration
HUGGINGFACE_API_KEY=your_key_here
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Chunking Parameters
CHUNK_SIZE=1000          # Characters per chunk
CHUNK_OVERLAP=100        # Overlap between chunks

# Retrieval Parameters
TOP_K=3                  # Number of chunks to retrieve

# Paths
DATA_DIR=./data
VECTOR_DB_PATH=./chroma_db
```

## 🎓 Design Decisions & Trade-offs

### Two-Pipeline Architecture
**Decision:** Separate Loading (offline) from Inference (runtime)
- ✅ **Benefits:** Independent optimization, flexible scaling
- ❌ **Trade-offs:** Increased complexity, delayed document updates

### Local Embeddings
**Decision:** SentenceTransformer (local) vs OpenAI API
- ✅ **Benefits:** Zero cost, complete privacy, no rate limits
- ❌ **Trade-offs:** Lower quality than OpenAI embeddings (384 vs 1536 dims)

### ChromaDB
**Decision:** ChromaDB vs Pinecone/FAISS/Weaviate
- ✅ **Benefits:** Simple API, open-source, flexible deployment
- ❌ **Trade-offs:** Limited scalability vs managed cloud services

### Mistral 7B
**Decision:** Mistral 7B vs GPT-4
- ✅ **Benefits:** 150× cheaper ($0.0002 vs $0.03 per 1K tokens)
- ❌ **Trade-offs:** Lower answer quality, less nuanced reasoning

### Chunk Size: 1000 Characters
**Decision:** 1000 chars with 100 overlap
- ✅ **Benefits:** Balanced context, fits embedding limits, good retrieval
- ❌ **Trade-offs:** Too small = noise, Too large = precision loss

### Top-k = 3 Chunks
**Decision:** Retrieve 3 chunks per query
- ✅ **Benefits:** Sufficient context, manageable token count
- ❌ **Trade-offs:** k=1 incomplete, k=10+ excessive noise

## 🔧 Troubleshooting

### "No PDF files found"
- Ensure PDFs are in `./data` directory
- Check file extensions are `.pdf`

### "Invalid API key"
- Verify HUGGINGFACE_API_KEY in `.env`
- Ensure token has read access
- Test at https://huggingface.co/settings/tokens

### "Model is loading"
- First API call may take 20-60 seconds
- Model loads on HuggingFace servers
- Subsequent calls are faster

### Slow Embedding Generation
- Normal for large documents (first run only)
- Consider GPU: Change `device: 'cpu'` to `'cuda'` in embedding_generator.py
- Results cached in ChromaDB for future runs

## 📊 Performance

**Loading Pipeline (one-time):**
- 100-page PDF: ~2-3 minutes (CPU)
- Creates ~200-300 chunks
- Cached in ChromaDB for instant future access

**Inference Pipeline (per query):**
- Retrieval: <1 second
- LLM generation: 2-5 seconds
- Total: ~3-6 seconds per query

## 🛠️ Technologies Used

- **LangChain** - RAG framework (document loading, chains, retrieval)
- **ChromaDB** - Vector database with HNSW indexing
- **SentenceTransformers** - Local embedding generation
- **HuggingFace** - LLM API (Mistral 7B)
- **PyPDF** - PDF text extraction

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- LangChain for RAG framework
- HuggingFace for model hosting
- ChromaDB for vector storage
- SentenceTransformers for embeddings
