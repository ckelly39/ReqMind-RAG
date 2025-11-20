# 🚀 ReqMind - Complete Installation Guide

## 🔴 **IMPORTANT: If You Got Dependency Conflicts**

If you saw errors about `langchain-core` version conflicts, **follow this guide carefully**.

---

## 📋 **What Happened?**

You have newer versions of LangChain packages already installed that conflict with the old versions in the original requirements.txt.

**Conflict Example:**
```
langchain-classic 1.0.0 requires langchain-core>=1.0.0, 
but you have langchain-core 0.1.23 which is incompatible.
```

---

## ✅ **Solution: Fresh Installation**

### **Option 1: Automated Installation (RECOMMENDED - Windows)**

```batch
REM Navigate to reqmind folder
cd reqmind

REM Activate virtual environment
venv\Scripts\activate

REM Run installation script
install_windows.bat
```

The script will:
1. ✅ Uninstall conflicting packages
2. ✅ Install compatible modern versions
3. ✅ Set up everything correctly

### **Option 2: Automated Installation (Mac/Linux)**

```bash
# Navigate to reqmind folder
cd reqmind

# Activate virtual environment
source venv/bin/activate

# Run installation script
./install_unix.sh
```

### **Option 3: Manual Installation**

If you prefer to install manually:

```bash
# 1. Activate virtual environment
cd reqmind
venv\Scripts\activate  # Windows
# OR: source venv/bin/activate  # Mac/Linux

# 2. Uninstall old versions
pip uninstall -y langchain langchain-community langchain-core langchain-text-splitters

# 3. Install modern compatible versions
pip install "langchain>=0.3.0"
pip install "langchain-community>=0.3.0"
pip install "langchain-core>=0.3.0"

# 4. Install other dependencies
pip install "chromadb>=0.4.22"
pip install "sentence-transformers>=2.3.1"
pip install "pypdf>=3.17.4"
pip install "huggingface-hub>=0.20.3"
pip install "requests>=2.31.0"
pip install "python-dotenv>=1.0.0"
pip install "typing-extensions>=4.12.0"
```

---

## 🎯 **Complete Setup (From Scratch)**

### **Step 1: Create Fresh Virtual Environment**

```bash
# Navigate to reqmind directory
cd path\to\reqmind

# Remove old virtual environment (if exists)
rmdir /s /q venv  # Windows
# OR: rm -rf venv  # Mac/Linux

# Create new virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# OR: source venv/bin/activate  # Mac/Linux
```

### **Step 2: Install Dependencies**

**Windows:**
```batch
install_windows.bat
```

**Mac/Linux:**
```bash
./install_unix.sh
```

**OR Manual:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 3: Configure**

```bash
# Copy configuration template
copy .env.example .env  # Windows
# OR: cp .env.example .env  # Mac/Linux

# Edit .env file
notepad .env  # Windows
# OR: nano .env  # Mac/Linux
```

Add your HuggingFace API key:
```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
```

Get free API key: https://huggingface.co/settings/tokens

### **Step 4: Add PDF Documents**

```bash
# Create data directory
mkdir data

# Copy your requirements PDF
copy "path\to\RequirementsDocument.pdf" data\  # Windows
# OR: cp /path/to/RequirementsDocument.pdf data/  # Mac/Linux
```

### **Step 5: Run!**

```bash
cd src
python main.py
```

---

## ✅ **Verify Installation**

Check that you have compatible versions:

```bash
pip list | findstr langchain  # Windows
# OR: pip list | grep langchain  # Mac/Linux
```

**You should see:**
```
langchain                    0.3.x
langchain-community          0.3.x
langchain-core               0.3.x
langchain-text-splitters     0.3.x
```

---

## 🐛 **Troubleshooting**

### **Problem: "ModuleNotFoundError: No module named 'langchain_text_splitters'"**

**Solution:**
```bash
pip install langchain-text-splitters>=0.3.0
```

### **Problem: Still getting version conflicts**

**Solution: Nuclear option (Clean slate)**
```bash
# 1. Deactivate virtual environment
deactivate

# 2. Delete virtual environment
rmdir /s /q venv  # Windows
# rm -rf venv  # Mac/Linux

# 3. Start fresh
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip

# 4. Install ONLY what we need
pip install "langchain>=0.3.0" "langchain-community>=0.3.0" "langchain-core>=0.3.0"
pip install chromadb sentence-transformers pypdf python-dotenv huggingface-hub requests
```

### **Problem: "No PDF files found"**

**Solution:**
```bash
# Ensure PDFs are in data folder
mkdir data
# Add your PDFs to this folder
```

### **Problem: "Invalid API key"**

**Solution:**
- Check `.env` file exists (not `.env.example`)
- Verify `HUGGINGFACE_API_KEY=hf_...` is set
- Get new key: https://huggingface.co/settings/tokens
- Make sure there are no spaces or quotes around the key

### **Problem: "Model is loading" (takes 30+ seconds)**

**Solution:**
- This is normal for first API call
- HuggingFace loads model on their servers
- Subsequent calls will be faster
- Just wait and it will work!

---

## 📊 **Expected Output**

After successful installation and running `python main.py`:

```
======================================================================
⚙️  CONFIGURATION
======================================================================

Config(model=mistralai/Mistral-7B-Instruct-v0.2, embedding=all-MiniLM-L6-v2, chunk_size=1000, api_key=hf_xxx...)


======================================================================
🔧 LOADING PIPELINE - Document Processing
======================================================================

Step 1: Document Parsing

Found 1 PDF file(s)
✓ Parsed 33 pages from RequirementsDocument.pdf
✓ Total: 33 pages extracted

Step 2: Text Splitting
✓ Split 33 documents into 145 chunks
  Chunk size: 1000 chars, Overlap: 100 chars

Step 3: Embedding Generation
Loading embedding model: all-MiniLM-L6-v2...
✓ Embedding model loaded: all-MiniLM-L6-v2

Step 4: Vector Store Creation
✓ VectorStore singleton instance created
  Location: C:\...\reqmind\chroma_db
  Collection: reqmind_collection

Creating vector store from 145 documents...
✓ Vector store created with 145 chunks

✓ Loading Pipeline Complete!

======================================================================
🚀 INFERENCE PIPELINE - Query Processing
======================================================================

Step 1: Retrieval Component
✓ RetrievalComponent initialized (top_k=3)

Step 2: LLM Initialization
✓ InferenceClient initialized for model: mistralai/Mistral-7B-Instruct-v0.2

Step 3: RetrievalQA Chain
✓ RetrievalQA chain created (chain_type='stuff')

Step 4: Client UI
======================================================================
🤖 ReqMind - Requirements Document Q&A System
======================================================================

Welcome! I can help you search through requirements documents.

Example questions you can ask:
  • What are the authentication requirements?
  • What is the maximum response time?
  • Tell me about the security requirements
  • What are the scalability requirements?

Commands:
  • 'exit' or 'quit' - Exit the system
  • 'history' - Show conversation history
  • 'clear' - Clear conversation history

----------------------------------------------------------------------

💬 Your question: 
```

---

## 🎉 **Success Checklist**

Before running, verify:

- [x] Virtual environment activated
- [x] All dependencies installed (no conflicts)
- [x] `.env` file exists with `HUGGINGFACE_API_KEY`
- [x] PDF files in `data/` directory
- [x] Python 3.8+ installed

---

## 📧 **Still Need Help?**

1. **Check Installation Scripts**: Use `install_windows.bat` or `install_unix.sh`
2. **Try Nuclear Option**: Delete venv and reinstall from scratch
3. **Verify Versions**: Run `pip list | grep langchain` to check versions
4. **Check Python Version**: Run `python --version` (need 3.8+)

---

## 🚀 **Quick Commands Summary**

```bash
# Fresh start (recommended for conflicts)
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
./install_unix.sh  # or install_windows.bat on Windows

# Configure
cp .env.example .env
# Edit .env with your API key

# Add PDFs
mkdir data
cp /path/to/pdf data/

# Run
cd src
python main.py
```

---

**After following this guide, your ReqMind system should work perfectly!** ✅
