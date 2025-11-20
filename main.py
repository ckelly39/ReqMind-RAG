"""Main application for ReqMind-RAG system."""

import argparse
from pathlib import Path
from document_ingester import DocumentIngester
from vector_store import VectorStoreManager
from rag_system import RAGQuerySystem
import config


def initialize_system(force_recreate: bool = False):
    """Initialize the RAG system.
    
    Args:
        force_recreate: Whether to force recreation of vector store
        
    Returns:
        Tuple of (vector_store_manager, rag_system)
    """
    print("=" * 60)
    print("Initializing ReqMind-RAG System")
    print("=" * 60)
    
    # Initialize vector store manager
    vs_manager = VectorStoreManager()
    
    # Check if we need to create/recreate the vector store
    if force_recreate or not config.CHROMA_DB_DIR.exists():
        print("\nIngesting documents...")
        ingester = DocumentIngester()
        documents = ingester.process_documents(config.DOCUMENTS_DIR)
        
        if not documents:
            print("\nNo documents found in documents/ directory.")
            print("Please add .txt files containing requirements documents.")
            return None, None
        
        # Create vector store
        vector_store = vs_manager.create_vector_store(documents)
    else:
        # Load existing vector store
        vector_store = vs_manager.load_vector_store()
        if vector_store is None:
            print("Failed to load vector store. Please run with --recreate flag.")
            return None, None
    
    # Initialize RAG system
    print("\nInitializing RAG Query System...")
    rag_system = RAGQuerySystem(vector_store, use_local_llm=True)
    
    print("\n" + "=" * 60)
    print("System initialized successfully!")
    print("=" * 60)
    
    return vs_manager, rag_system


def interactive_mode(rag_system):
    """Run interactive query mode.
    
    Args:
        rag_system: Initialized RAG query system
    """
    print("\n" + "=" * 60)
    print("Interactive Query Mode")
    print("=" * 60)
    print("Ask questions about your requirements documents.")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    while True:
        try:
            question = input("Question: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if not question:
                continue
            
            # Get response
            response = rag_system.query_with_context(question)
            
            # Display answer
            print("\n" + "-" * 60)
            print("Answer:")
            print(response["answer"])
            
            # Display sources
            if response["sources"]:
                print("\nSources:")
                for i, source in enumerate(response["sources"], 1):
                    print(f"\n  [{i}] {source['metadata'].get('source', 'Unknown')}")
                    print(f"      {source['content'][:200]}...")
            
            print("-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def single_query_mode(rag_system, question: str):
    """Process a single query and exit.
    
    Args:
        rag_system: Initialized RAG query system
        question: Question to ask
    """
    response = rag_system.query_with_context(question)
    
    print("\n" + "=" * 60)
    print("Answer:")
    print("=" * 60)
    print(response["answer"])
    
    if response["sources"]:
        print("\n" + "=" * 60)
        print("Sources:")
        print("=" * 60)
        for i, source in enumerate(response["sources"], 1):
            print(f"\n[{i}] Source: {source['metadata'].get('source', 'Unknown')}")
            print(f"    Content: {source['content'][:300]}...")
    print("\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ReqMind-RAG: Query requirements documents using natural language"
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Force recreation of vector store from documents"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Single query to process (non-interactive mode)"
    )
    
    args = parser.parse_args()
    
    # Initialize system
    vs_manager, rag_system = initialize_system(force_recreate=args.recreate)
    
    if rag_system is None:
        return
    
    # Run appropriate mode
    if args.query:
        single_query_mode(rag_system, args.query)
    else:
        interactive_mode(rag_system)


if __name__ == "__main__":
    main()
