# ReqMind - Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Setup Environment (2 minutes)

```bash
# Navigate to project directory
cd reqmind

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure (1 minute)

```bash
# Copy configuration template
cp .env.example .env

# Edit .env and add your HuggingFace API key
# Get key from: https://huggingface.co/settings/tokens
```

Your `.env` should look like:
```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
TOP_K=3
DATA_DIR=./data
VECTOR_DB_PATH=./chroma_db
```

## Step 3: Add PDF Documents (30 seconds)

```bash
# Create data directory
mkdir -p data

# Copy your requirements PDF
cp /path/to/your/RequirementsDocument.pdf data/
```

## Step 4: Run! (30 seconds)

```bash
cd src
python main.py
```

## What Happens Next?

**First Run:**
1. Loads your PDFs (5-10 seconds)
2. Splits into chunks (2-3 seconds)
3. Generates embeddings (1-2 minutes for 100 pages)
4. Saves to ChromaDB (5 seconds)
5. Starts interactive Q&A

**Subsequent Runs:**
- Loads from cached ChromaDB instantly!
- No need to reprocess documents

## Example Questions

Try asking:
- "What are the authentication requirements?"
- "What is the maximum response time?"
- "Tell me about security requirements"
- "What are the scalability goals?"

## Quick Commands

- `exit` or `quit` - Exit the system
- `history` - See previous questions
- `clear` - Clear history

## Troubleshooting

**"No module named 'langchain'"**
→ Install dependencies: `pip install -r requirements.txt`

**"No PDF files found"**
→ Put PDFs in `./data` directory

**"Invalid API key"**
→ Check HUGGINGFACE_API_KEY in `.env` file

**"Model is loading"**
→ First API call takes 20-60 seconds (one-time wait)

## Success! 🎉

You should now see:
```
🤖 ReqMind - Requirements Document Q&A System
======================================================================

Welcome! I can help you search through requirements documents.

💬 Your question: 
```

Start asking questions about your requirements!

## Need Help?

- Read full README.md for detailed documentation
- Check configuration in .env file
- Ensure PDFs are in data/ directory
- Verify HuggingFace API key is valid

---

**Total Setup Time: ~5 minutes**
(First run adds 2-3 minutes for embedding generation)
