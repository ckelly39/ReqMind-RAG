# ReqMind-RAG Usage Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- 4GB+ RAM (for running local models)
- ~1GB disk space (for models)
- Internet connection (first-time setup only)

### First-Time Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Download Models** (One-time, requires internet)
```bash
python setup.py
```

This will download:
- Sentence Transformer embedding model (~100MB)
- FLAN-T5 language model (~300MB)

## Quick Start

### 1. Prepare Your Documents

Place your requirements documents in the `documents/` directory:

```bash
documents/
  ├── functional_requirements.txt
  ├── nonfunctional_requirements.txt
  └── security_requirements.txt
```

**Document Format**: Plain text (.txt) files work best. Each document should contain your requirements in any format (structured or unstructured).

**Sample documents are already included** to help you get started!

### 2. Run the System

#### Interactive Mode (Recommended for Exploration)

```bash
python main.py
```

This starts a chat-like interface where you can ask multiple questions:

```
Question: What are the authentication requirements?
Answer: The system shall authenticate users using email and password...

Question: What is the required uptime?
Answer: The system shall maintain 99.9% uptime availability...
```

#### Single Query Mode (Good for Scripts)

```bash
python main.py --query "What payment methods are supported?"
```

Returns a single answer and exits.

#### Force Rebuild (After Adding New Documents)

```bash
python main.py --recreate
```

Rebuilds the vector database with all documents.

## Usage Examples

### Example 1: Finding Security Requirements

```bash
$ python main.py --query "What are the security requirements?"
```

**Expected Output:**
```
============================================================
Answer:
============================================================
The system must encrypt data at rest using AES-256 and in transit
using TLS 1.3. Passwords shall be hashed using bcrypt or Argon2,
and sessions must timeout after 30 minutes of inactivity.

============================================================
Sources:
============================================================

[1] Source: nonfunctional_requirements.txt
    Content: NFR-004: Data Encryption
    The system shall encrypt all sensitive data at rest using AES-256...

[2] Source: nonfunctional_requirements.txt
    Content: NFR-005: Authentication Security
    The system shall implement secure password hashing...
```

### Example 2: Interactive Session

```bash
$ python main.py

============================================================
Interactive Query Mode
============================================================

Question: What browsers must be supported?

------------------------------------------------------------
Answer:
The system shall support the latest two versions of Chrome,
Firefox, Safari, and Edge browsers.

Sources:
  [1] nonfunctional_requirements.txt
      NFR-016: Browser Support...
------------------------------------------------------------

Question: What is the required response time?

------------------------------------------------------------
Answer:
The system shall respond to user requests within 2 seconds
under normal load conditions.

Sources:
  [1] nonfunctional_requirements.txt
      NFR-001: Response Time...
------------------------------------------------------------

Question: exit
Goodbye!
```

### Example 3: Adding New Documents

1. Add your `.txt` file to `documents/`:
```bash
cp my_new_requirements.txt documents/
```

2. Rebuild the vector database:
```bash
python main.py --recreate
```

3. Start querying:
```bash
python main.py
```

## Advanced Usage

### Running Example Scripts

```bash
python examples.py
```

This demonstrates:
- Basic programmatic usage
- Similarity search
- Batch query processing

### Testing the System

```bash
python test_system.py
```

Runs basic tests to verify the system is working correctly.

### Customizing Configuration

Edit `config.py` to customize:

```python
# Chunk size for document processing
CHUNK_SIZE = 500        # Larger = more context, slower
CHUNK_OVERLAP = 50      # Overlap between chunks

# Number of similar documents to retrieve
TOP_K_RESULTS = 3       # More = more context, slower

# Embedding model (from HuggingFace)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

### Using Different Models

To use a different embedding model, edit `config.py`:

```python
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # Better quality, slower
```

Then rebuild:
```bash
python main.py --recreate
```

## Programmatic Usage

You can use ReqMind-RAG in your own Python scripts:

```python
from document_ingester import DocumentIngester
from vector_store import VectorStoreManager
from rag_system import RAGQuerySystem
import config

# 1. Load and process documents
ingester = DocumentIngester()
documents = ingester.process_documents(config.DOCUMENTS_DIR)

# 2. Create vector store
vs_manager = VectorStoreManager()
vector_store = vs_manager.create_vector_store(documents)

# 3. Initialize RAG system
rag = RAGQuerySystem(vector_store)

# 4. Ask questions
response = rag.query_with_context("What are the main features?")
print(response['answer'])

# Access sources
for source in response['sources']:
    print(f"Source: {source['metadata']['source']}")
    print(f"Content: {source['content']}")
```

## Troubleshooting

### "No module named 'langchain'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "We couldn't connect to 'https://huggingface.co'"

**Solution**: Run the setup script with internet connection
```bash
python setup.py
```

### "No documents found"

**Solution**: Add `.txt` files to the `documents/` directory
```bash
ls documents/*.txt
```

### Slow Performance

**Solutions**:
1. Reduce `CHUNK_SIZE` in `config.py`
2. Reduce `TOP_K_RESULTS` in `config.py`
3. Use a smaller embedding model
4. Ensure models are cached (run `setup.py`)

### Out of Memory

**Solutions**:
1. Reduce `CHUNK_SIZE` in `config.py` to 300
2. Process fewer documents at once
3. Use a smaller model

## Tips for Best Results

### Document Formatting
- Use clear section headers
- Include requirement IDs (e.g., REQ-001, NFR-001)
- Keep paragraphs focused on single topics

### Query Phrasing
- Be specific: "What are the password requirements?" vs "Tell me about passwords"
- Use domain terminology: "authentication requirements" vs "login stuff"
- Ask one question at a time

### Example Good Queries
- "What are the security requirements for payment processing?"
- "What is the required system uptime?"
- "How should user sessions be managed?"
- "What browsers must be supported?"
- "What are the performance requirements?"

### Example Poor Queries
- "Tell me everything" (too broad)
- "Stuff about users" (too vague)
- "Requirements" (too general)

## Next Steps

1. **Add your own requirements documents** to the `documents/` directory
2. **Run setup.py** to download models (if not done already)
3. **Rebuild the database** with `python main.py --recreate`
4. **Start querying** with `python main.py`

## Support

For issues or questions:
1. Check this usage guide
2. Run `python test_system.py` to verify installation
3. Check the README.md for more information
4. Review the example scripts in `examples.py`
