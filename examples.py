#!/usr/bin/env python3
"""
Example usage script for ReqMind-RAG system.
Demonstrates how to use the system programmatically.
"""

from pathlib import Path
from document_ingester import DocumentIngester
from vector_store import VectorStoreManager
from rag_system import RAGQuerySystem
import config


def example_basic_usage():
    """Basic usage example."""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    
    # Step 1: Initialize document ingester
    ingester = DocumentIngester()
    documents = ingester.process_documents(config.DOCUMENTS_DIR)
    print(f"\n✓ Processed {len(documents)} document chunks")
    
    # Step 2: Create vector store
    vs_manager = VectorStoreManager()
    vector_store = vs_manager.create_vector_store(documents)
    print("✓ Vector store created")
    
    # Step 3: Initialize RAG system
    rag = RAGQuerySystem(vector_store)
    print("✓ RAG system initialized")
    
    # Step 4: Ask questions
    questions = [
        "What are the authentication requirements?",
        "What is the required system uptime?",
        "How should passwords be stored?"
    ]
    
    for question in questions:
        print(f"\n{'─' * 70}")
        print(f"Q: {question}")
        response = rag.query_with_context(question)
        print(f"A: {response['answer']}")
        print(f"   Sources: {len(response['sources'])} documents")
    
    print("\n" + "=" * 70)


def example_similarity_search():
    """Example of direct similarity search."""
    print("\n" + "=" * 70)
    print("Example 2: Similarity Search")
    print("=" * 70)
    
    # Load existing vector store
    vs_manager = VectorStoreManager()
    vector_store = vs_manager.load_vector_store()
    
    if vector_store:
        query = "security and encryption"
        results = vs_manager.similarity_search(query, k=3)
        
        print(f"\nSearch query: '{query}'")
        print(f"Found {len(results)} similar documents:\n")
        
        for i, doc in enumerate(results, 1):
            print(f"{i}. Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"   Content: {doc.page_content[:150]}...")
            print()
    else:
        print("No existing vector store found. Run example_basic_usage() first.")
    
    print("=" * 70)


def example_batch_queries():
    """Example of processing multiple queries."""
    print("\n" + "=" * 70)
    print("Example 3: Batch Query Processing")
    print("=" * 70)
    
    # Load existing vector store
    vs_manager = VectorStoreManager()
    vector_store = vs_manager.load_vector_store()
    
    if vector_store:
        rag = RAGQuerySystem(vector_store)
        
        queries = [
            "What payment methods are supported?",
            "What are the performance requirements?",
            "How is user data protected?",
            "What browsers are supported?",
            "What is the backup strategy?"
        ]
        
        print(f"\nProcessing {len(queries)} queries...\n")
        
        for i, query in enumerate(queries, 1):
            response = rag.query(query)
            print(f"{i}. {query}")
            print(f"   → {response['result'][:100]}...")
            print()
    else:
        print("No existing vector store found. Run example_basic_usage() first.")
    
    print("=" * 70)


def main():
    """Run all examples."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  ReqMind-RAG: Example Usage Demonstrations".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    try:
        # Run examples
        example_basic_usage()
        example_similarity_search()
        example_batch_queries()
        
        print("\n" + "=" * 70)
        print("All examples completed successfully! ✓")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
