#!/usr/bin/env python3
"""
Simple test script for ReqMind-RAG system.
Tests basic functionality without requiring model downloads.
"""

from pathlib import Path
import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from document_ingester import DocumentIngester
        from vector_store import VectorStoreManager
        from rag_system import RAGQuerySystem
        import config
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_document_ingestion():
    """Test document loading and chunking."""
    print("\nTesting document ingestion...")
    try:
        from document_ingester import DocumentIngester
        import config
        
        ingester = DocumentIngester()
        documents = ingester.load_documents(config.DOCUMENTS_DIR)
        
        if not documents:
            print("✗ No documents found")
            return False
        
        print(f"✓ Loaded {len(documents)} documents")
        
        chunks = ingester.split_documents(documents)
        print(f"✓ Split into {len(chunks)} chunks")
        
        return True
    except Exception as e:
        print(f"✗ Document ingestion error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration settings."""
    print("\nTesting configuration...")
    try:
        import config
        
        print(f"✓ Documents directory: {config.DOCUMENTS_DIR}")
        print(f"✓ ChromaDB directory: {config.CHROMA_DB_DIR}")
        print(f"✓ Embedding model: {config.EMBEDDING_MODEL}")
        print(f"✓ Chunk size: {config.CHUNK_SIZE}")
        print(f"✓ Top-K results: {config.TOP_K_RESULTS}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'main.py',
        'config.py',
        'document_ingester.py',
        'vector_store.py',
        'rag_system.py',
        'requirements.txt',
        'README.md',
        'examples.py'
    ]
    
    base_dir = Path(__file__).parent
    all_exist = True
    
    for filename in required_files:
        filepath = base_dir / filename
        if filepath.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False
    
    # Check documents directory
    docs_dir = base_dir / 'documents'
    if docs_dir.exists():
        txt_files = list(docs_dir.glob('*.txt'))
        print(f"✓ documents/ directory exists with {len(txt_files)} .txt files")
    else:
        print("✗ documents/ directory missing")
        all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("=" * 70)
    print("ReqMind-RAG System Tests")
    print("=" * 70)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Document Ingestion", test_document_ingestion),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "=" * 70)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 70)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
