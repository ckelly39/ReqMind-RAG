# ReqMind-RAG Project Overview

## 🎯 Project Purpose

ReqMind-RAG is a **Retrieval-Augmented Generation (RAG) system** designed to enable natural language querying of software requirements documents. Instead of manually searching through requirement documents, users can ask questions in plain English and get intelligent answers with source citations.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
│                    (main.py CLI)                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   RAG Query System                           │
│                   (rag_system.py)                           │
│  • Receives natural language questions                      │
│  • Retrieves relevant context                               │
│  • Generates answers using LLM                              │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────┐   ┌──────────────────────┐
│   Vector Store       │   │   Language Model     │
│  (vector_store.py)   │   │   (FLAN-T5-Small)   │
│                      │   │                      │
│  • ChromaDB          │   │  • Text generation   │
│  • Embeddings        │   │  • Q&A synthesis     │
│  • Similarity search │   │                      │
└──────────────────────┘   └──────────────────────┘
            ▲
            │
┌──────────────────────┐
│ Document Ingester    │
│(document_ingester.py)│
│                      │
│  • Load .txt files   │
│  • Text chunking     │
│  • Preprocessing     │
└──────────────────────┘
            ▲
            │
┌──────────────────────┐
│  Requirements Docs   │
│   (documents/)       │
│                      │
│  • .txt files        │
└──────────────────────┘
```

## 📁 Project Structure

```
ReqMind-RAG/
│
├── 📄 Core Application Files
│   ├── main.py                    # Main CLI application
│   ├── config.py                  # Configuration settings
│   ├── document_ingester.py       # Document loading & chunking
│   ├── vector_store.py           # ChromaDB vector database
│   └── rag_system.py             # RAG query system
│
├── 📚 Documentation
│   ├── README.md                  # Main documentation
│   ├── USAGE.md                   # Detailed usage guide
│   └── PROJECT_OVERVIEW.md        # This file
│
├── 🔧 Utilities
│   ├── setup.py                   # Model download script
│   ├── examples.py               # Usage examples
│   └── test_system.py            # System tests
│
├── 📋 Configuration
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                # Git ignore rules
│
└── 📁 Data Directories
    ├── documents/                 # Input: Requirements .txt files
    │   ├── ecommerce_requirements.txt
    │   └── nonfunctional_requirements.txt
    └── chroma_db/                # Output: Vector database (auto-generated)
```

## 🔄 Workflow

### 1️⃣ Setup Phase (One-time)
```
pip install -r requirements.txt
         ↓
python setup.py (downloads models)
         ↓
Models cached locally
```

### 2️⃣ Indexing Phase
```
User adds .txt files to documents/
         ↓
DocumentIngester loads & chunks files
         ↓
VectorStoreManager creates embeddings
         ↓
ChromaDB stores vector representations
```

### 3️⃣ Query Phase
```
User asks: "What are the security requirements?"
         ↓
Question → Embedding
         ↓
Vector similarity search finds relevant chunks
         ↓
Retrieved context + Question → LLM
         ↓
LLM generates answer
         ↓
Answer + Source citations returned to user
```

## 🧩 Components

### 1. Document Ingester (`document_ingester.py`)
- **Purpose**: Load and prepare requirements documents
- **Key Features**:
  - Loads .txt files from documents/ directory
  - Splits large documents into manageable chunks (500 chars default)
  - Maintains overlap between chunks for context continuity
  - Preserves source metadata

### 2. Vector Store Manager (`vector_store.py`)
- **Purpose**: Manage semantic search capabilities
- **Key Features**:
  - Uses HuggingFace Sentence Transformers for embeddings
  - Stores embeddings in ChromaDB
  - Performs similarity search
  - Persists database to disk
  - Supports incremental document addition

### 3. RAG Query System (`rag_system.py`)
- **Purpose**: Answer questions using retrieved context
- **Key Features**:
  - Retrieves top-K most relevant document chunks
  - Formats context for LLM
  - Uses FLAN-T5 for answer generation
  - Returns answers with source citations

### 4. Main Application (`main.py`)
- **Purpose**: User interface
- **Key Features**:
  - Interactive chat mode
  - Single query mode
  - Force rebuild option
  - User-friendly output formatting

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | LangChain | RAG orchestration & document processing |
| **Vector DB** | ChromaDB | Efficient similarity search |
| **Embeddings** | HuggingFace Sentence Transformers | Convert text to vectors |
| **LLM** | FLAN-T5-Small | Answer generation |
| **Language** | Python 3.8+ | Core implementation |

## 📊 Data Flow

```
Input Document (.txt)
    │
    ├─► Load Text
    │
    ├─► Split into Chunks
    │       │
    │       ├─► Chunk 1: "REQ-001: User Registration..."
    │       ├─► Chunk 2: "REQ-002: User Login..."
    │       └─► Chunk 3: "REQ-003: Password Recovery..."
    │
    └─► Generate Embeddings
            │
            ├─► Vector 1: [0.23, -0.45, 0.67, ...]
            ├─► Vector 2: [0.12, -0.34, 0.56, ...]
            └─► Vector 3: [0.45, -0.23, 0.78, ...]
                    │
                    └─► Store in ChromaDB

Query: "What are the authentication requirements?"
    │
    ├─► Convert to Embedding: [0.21, -0.43, 0.65, ...]
    │
    ├─► Find Similar Vectors
    │       │
    │       └─► Top 3 Matches: Chunk 1, Chunk 2, Chunk 5
    │
    ├─► Combine Context + Question
    │
    ├─► LLM Processing
    │
    └─► Generate Answer + Citations
```

## 🎯 Use Cases

### 1. Requirements Analysis
- **Scenario**: Developer needs to understand authentication requirements
- **Solution**: Ask "What are the authentication requirements?"
- **Benefit**: Instant answer instead of reading entire document

### 2. Compliance Checking
- **Scenario**: Verify security standards compliance
- **Solution**: Ask "What encryption standards must be used?"
- **Benefit**: Quick verification with source citations

### 3. New Team Member Onboarding
- **Scenario**: New developer needs to understand system requirements
- **Solution**: Interactive Q&A session
- **Benefit**: Self-service knowledge discovery

### 4. Requirements Review
- **Scenario**: Product manager reviewing feature completeness
- **Solution**: Ask specific questions about features
- **Benefit**: Targeted information retrieval

## 🚀 Getting Started

```bash
# 1. Setup (one-time)
pip install -r requirements.txt
python setup.py

# 2. Add your requirements documents
cp your_requirements.txt documents/

# 3. Run the system
python main.py

# 4. Ask questions
Question: What are the performance requirements?
```

## 🔍 Example Interactions

### Example 1: Security Query
```
Q: What security measures are required for payment processing?

A: The system must comply with PCI-DSS Level 1 requirements. Credit 
   card information shall never be stored in the database. All payment 
   processing must use secure, compliant methods.

Sources:
  [1] nonfunctional_requirements.txt - NFR-007: Payment Security
  [2] ecommerce_requirements.txt - REQ-009: Payment Processing
```

### Example 2: Performance Query
```
Q: What is the required system response time?

A: The system shall respond to user requests within 2 seconds under 
   normal load conditions. Page load time shall not exceed 3 seconds 
   for 95% of requests.

Sources:
  [1] nonfunctional_requirements.txt - NFR-001: Response Time
```

## 🧪 Testing

```bash
# Run system tests
python test_system.py

# Run examples
python examples.py

# Test single query
python main.py --query "What are the main features?"
```

## 📈 Future Enhancements

Potential improvements:
- [ ] Support for PDF and Word documents
- [ ] Multi-language support
- [ ] Web-based UI
- [ ] Requirements traceability
- [ ] Version comparison
- [ ] Export to various formats
- [ ] Integration with issue trackers
- [ ] Automated requirements validation

## 📝 Best Practices

### Document Preparation
1. Use clear, structured text format
2. Include requirement IDs (REQ-001, NFR-001, etc.)
3. Keep related requirements together
4. Use consistent terminology

### Query Formulation
1. Be specific in your questions
2. Use domain terminology from your documents
3. Ask one question at a time
4. Reference specific topics (e.g., "security", "performance")

### System Maintenance
1. Rebuild vector store after adding new documents
2. Monitor disk space for ChromaDB
3. Keep models updated periodically
4. Backup your documents directory

## 🤝 Contributing

To extend this system:
1. Review the code structure above
2. Understand the data flow
3. Make focused changes to individual modules
4. Test with `test_system.py`
5. Update documentation

## 📄 License

MIT License - See repository for details

---

**Built with ❤️ using LangChain, ChromaDB, and HuggingFace**
