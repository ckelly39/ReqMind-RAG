# ReqMind-RAG

A Retrieval-Augmented Generation (RAG) system for querying software requirements documents using natural language. Built with LangChain, ChromaDB, and HuggingFace.

## Features

- 📄 **Document Ingestion**: Load and process requirements documents from text files
- 🔍 **Semantic Search**: Find relevant requirements using natural language queries
- 🤖 **AI-Powered Q&A**: Get intelligent answers about your requirements using local LLM
- 💾 **Vector Storage**: Efficient document storage and retrieval with ChromaDB
- 🔄 **Interactive Mode**: Chat-like interface for continuous querying
- ⚡ **Fast & Local**: Runs entirely on your machine using HuggingFace models

## Technology Stack

- **LangChain**: Framework for building RAG applications
- **ChromaDB**: Vector database for semantic search
- **HuggingFace**: Embeddings (all-MiniLM-L6-v2) and LLM (FLAN-T5)
- **Sentence Transformers**: Document embeddings generation

## Installation

### Prerequisites
- Python 3.8 or higher
- 4GB+ RAM
- ~1GB disk space for models
- **Internet connection** (required for first-time model download)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/ckelly39/ReqMind-RAG.git
cd ReqMind-RAG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Download models** (one-time, requires internet):
```bash
python setup.py
```

This downloads:
- Sentence Transformer embedding model (~100MB)
- FLAN-T5 language model (~300MB)

**Note**: After initial setup, the system can run completely offline as models are cached locally.

## Quick Start

### 1. Add Your Requirements Documents

Place your requirements documents (`.txt` files) in the `documents/` directory:

```bash
documents/
  ├── functional_requirements.txt
  ├── nonfunctional_requirements.txt
  └── api_requirements.txt
```

**Note**: Sample documents are provided to help you get started.

### 2. Run the System

**Interactive Mode** (Recommended):
```bash
python main.py
```

This will:
- Load and process your documents
- Create embeddings and vector store
- Start an interactive query session

**Single Query Mode**:
```bash
python main.py --query "What are the authentication requirements?"
```

**Force Recreate Vector Store**:
```bash
python main.py --recreate
```

## Usage Examples

### Interactive Mode

```
$ python main.py

============================================================
Initializing ReqMind-RAG System
============================================================

Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
Loaded 2 documents from documents/
Split into 45 chunks
Creating vector store with 45 documents...
Vector store created successfully

Initializing RAG Query System...
Initializing local LLM pipeline...
Local LLM initialized
Creating QA chain...
QA chain created

============================================================
System initialized successfully!
============================================================

============================================================
Interactive Query Mode
============================================================
Ask questions about your requirements documents.
Type 'exit' or 'quit' to end the session.

Question: What are the security requirements for payment processing?

------------------------------------------------------------
Answer:
The system must comply with PCI-DSS Level 1 requirements and shall not store credit card information in the database. All payment processing shall use secure, compliant methods.

Sources:

  [1] nonfunctional_requirements.txt
      NFR-007: Payment Security
      All payment processing shall comply with PCI-DSS Level 1 requirements.
      Credit card information shall never be stored in the system database...

  [2] ecommerce_requirements.txt
      REQ-009: Payment Processing
      The system shall support multiple payment methods including credit cards, debit cards, and digital wallets...
------------------------------------------------------------

Question: What is the required system uptime?

------------------------------------------------------------
Answer:
The system shall maintain 99.9% uptime availability with planned maintenance windows not exceeding 4 hours per month.

Sources:

  [1] nonfunctional_requirements.txt
      NFR-008: System Availability
      The system shall maintain 99.9% uptime availability...
------------------------------------------------------------
```

### Single Query Mode

```bash
$ python main.py --query "What authentication methods are supported?"

============================================================
Answer:
============================================================
The system supports authentication using email and password credentials, with optional multi-factor authentication (MFA) as an additional security feature.

============================================================
Sources:
============================================================

[1] Source: ecommerce_requirements.txt
    Content: REQ-002: User Login
    The system shall authenticate users using email and password credentials.
    The system shall support multi-factor authentication (MFA) as an optional security feature...
```

## Project Structure

```
ReqMind-RAG/
├── main.py                  # Main application entry point
├── config.py                # Configuration settings
├── document_ingester.py     # Document loading and chunking
├── vector_store.py          # ChromaDB vector store management
├── rag_system.py           # RAG query system with LangChain
├── requirements.txt         # Python dependencies
├── documents/              # Your requirements documents (.txt)
│   ├── ecommerce_requirements.txt
│   └── nonfunctional_requirements.txt
├── chroma_db/              # Vector database (auto-generated)
└── README.md
```

## Configuration

Edit `config.py` to customize:

- **EMBEDDING_MODEL**: HuggingFace embedding model (default: `all-MiniLM-L6-v2`)
- **CHUNK_SIZE**: Text chunk size for processing (default: `500`)
- **CHUNK_OVERLAP**: Overlap between chunks (default: `50`)
- **TOP_K_RESULTS**: Number of similar documents to retrieve (default: `3`)

## How It Works

1. **Document Ingestion**: 
   - Loads `.txt` files from `documents/` directory
   - Splits documents into smaller chunks for better retrieval

2. **Embedding Generation**:
   - Converts text chunks into vector embeddings using HuggingFace model
   - Stores embeddings in ChromaDB vector database

3. **Query Processing**:
   - Takes natural language question
   - Converts question to embedding
   - Retrieves most similar document chunks

4. **Answer Generation**:
   - Uses FLAN-T5 model to generate answer
   - Combines retrieved context with question
   - Returns answer with source documents

## Advanced Usage

### Adding New Documents

1. Add `.txt` files to `documents/` directory
2. Run with `--recreate` flag to rebuild vector store:
```bash
python main.py --recreate
```

### Using Custom LLM

Edit `rag_system.py` to configure different models or use HuggingFace API:

```python
# In rag_system.py, modify _initialize_llm method
# For HuggingFace API (requires API token):
rag_system = RAGQuerySystem(vector_store, use_local_llm=False)
```

## Requirements

- Python 3.8+
- 4GB+ RAM (for running local models)
- Internet connection (first run only, for downloading models)

## Troubleshooting

**Issue**: "No documents found"
- **Solution**: Add `.txt` files to `documents/` directory

**Issue**: Out of memory errors
- **Solution**: Reduce `CHUNK_SIZE` in `config.py` or use a smaller embedding model

**Issue**: Slow response times
- **Solution**: The first run downloads models (~500MB). Subsequent runs are faster.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [ChromaDB](https://www.trychroma.com/)
- Models from [HuggingFace](https://huggingface.co/)
