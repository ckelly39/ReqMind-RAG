#!/usr/bin/env python3
"""
Setup script to download and cache models for offline use.
Run this script once with internet connection to prepare the system.
"""

import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from transformers import pipeline

def setup_embedding_model():
    """Download and cache the embedding model."""
    print("=" * 70)
    print("Downloading Embedding Model")
    print("=" * 70)
    
    try:
        print("\nDownloading sentence-transformers/all-MiniLM-L6-v2...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✓ Embedding model downloaded and cached")
        return True
    except Exception as e:
        print(f"✗ Error downloading embedding model: {e}")
        return False

def setup_llm_model():
    """Download and cache the LLM model."""
    print("\n" + "=" * 70)
    print("Downloading Language Model")
    print("=" * 70)
    
    try:
        print("\nDownloading google/flan-t5-small...")
        qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            max_length=512
        )
        print("✓ Language model downloaded and cached")
        
        # Test the model
        print("\nTesting model...")
        test_result = qa_pipeline("What is 2+2?")
        print(f"Test result: {test_result}")
        
        return True
    except Exception as e:
        print(f"✗ Error downloading language model: {e}")
        return False

def main():
    """Main setup function."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  ReqMind-RAG Setup: Model Download".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\nThis script will download and cache the required models.")
    print("This needs to be done ONCE with an active internet connection.")
    print("After this, the system can run offline.\n")
    
    input("Press Enter to continue...")
    
    results = []
    
    # Download embedding model
    results.append(("Embedding Model", setup_embedding_model()))
    
    # Download LLM model
    results.append(("Language Model", setup_llm_model()))
    
    # Summary
    print("\n" + "=" * 70)
    print("Setup Summary")
    print("=" * 70)
    
    for component, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {component}")
    
    all_success = all(success for _, success in results)
    
    print("\n" + "=" * 70)
    if all_success:
        print("Setup completed successfully!")
        print("You can now run the system with: python main.py")
    else:
        print("Setup encountered errors. Please check your internet connection.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
