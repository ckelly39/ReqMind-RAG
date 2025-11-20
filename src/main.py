"""
ReqMind - Requirements Document Q&A System
Main entry point that initializes all components and runs the system.
"""

import sys
from pathlib import Path


def _enable_unicode_output() -> None:
    """
    Windows terminals often default to cp1252 and choke on emoji.
    Force stdout/stderr to utf-8 so our fancy status icons don't crash.
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


_enable_unicode_output()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from document_parser import DocumentParser
from text_splitter import TextSplitter
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from retrieval_component import RetrievalComponent
from llm import HuggingFaceInferenceLLM
from retrieval_qa import RetrievalQAComponent
from client_ui import ClientUI


def initialize_loading_pipeline(config: Config) -> VectorStore:
    """
    Initialize and run the Loading Pipeline.
    Processes documents and creates vector store.
    
    Args:
        config: Configuration object
        
    Returns:
        Initialized VectorStore instance
    """
    print("\n" + "=" * 70)
    print("🔧 LOADING PIPELINE - Document Processing")
    print("=" * 70 + "\n")
    
    # Step 1: Document Parser (LangChain PyPDFLoader)
    print("Step 1: Document Parsing")
    parser = DocumentParser()
    documents = parser.parse_directory(config.get_data_dir())
    
    # Step 2: Text Splitter (LangChain RecursiveCharacterTextSplitter)
    print("Step 2: Text Splitting")
    splitter = TextSplitter(
        chunk_size=config.get_chunk_size(),
        chunk_overlap=config.get_chunk_overlap()
    )
    chunks = splitter.split_documents(documents)
    
    # Step 3: Embedding Generator (Local SentenceTransformer)
    print("Step 3: Embedding Generation")
    embedding_generator = EmbeddingGenerator(
        model_name=config.get_embedding_model()
    )
    
    # Step 4: Vector Store (ChromaDB with Singleton pattern)
    print("Step 4: Vector Store Creation")
    vector_store = VectorStore(
        embeddings=embedding_generator.embeddings,
        persist_directory=config.get_vector_db_path(),
        collection_name="rag_301480610"
    )
    
    # Check if we can load existing store
    if not vector_store.load_existing():
        # Create new vector store from documents
        vector_store.create_from_documents(chunks)
        vector_store.persist()
    
    print("✓ Loading Pipeline Complete!\n")
    return vector_store


def initialize_inference_pipeline(config: Config, vector_store: VectorStore):
    """
    Initialize the Inference Pipeline.
    Sets up retrieval and generation components.
    
    Args:
        config: Configuration object
        vector_store: Initialized VectorStore instance
        
    Returns:
        Tuple of (RetrievalQAComponent, ClientUI)
    """
    print("=" * 70)
    print("🚀 INFERENCE PIPELINE - Query Processing")
    print("=" * 70 + "\n")
    
    # Step 1: Retrieval Component
    print("Step 1: Retrieval Component")
    retrieval_component = RetrievalComponent(
        vector_store=vector_store,
        top_k=config.get_top_k()
    )
    
    # Step 2: Custom LLM with InferenceClient (Adapter pattern)
    print("Step 2: LLM Initialization")
    llm = HuggingFaceInferenceLLM(
        api_key=config.get_api_key(),
        model_name=config.get_model_name()
    )
    
    # Step 3: RetrievalQA (LangChain chain with "stuff" strategy)
    print("Step 3: RetrievalQA Chain")
    retrieval_qa = RetrievalQAComponent(
        llm=llm,
        retrieval_component=retrieval_component
    )
    
    # Step 4: Client UI
    print("Step 4: Client UI")
    client_ui = ClientUI(retrieval_qa=retrieval_qa)
    
    print("✓ Inference Pipeline Complete!\n")
    return retrieval_qa, client_ui


def main():
    """
    Main function: Initialize system and start interactive session.
    """
    try:
        # Print startup message (Task 5a)
        print("\nStarting Kelly RAG Chatbot setup..")
        
        # Load configuration
        print("\n" + "=" * 70)
        print("⚙️  CONFIGURATION")
        print("=" * 70 + "\n")
        config = Config()
        print(config)
        print()
        
        # Initialize Loading Pipeline
        vector_store = initialize_loading_pipeline(config)
        
        # Initialize Inference Pipeline
        retrieval_qa, client_ui = initialize_inference_pipeline(config, vector_store)
        
        # Print ready message (Task 5b)
        print("RAG Chatbot Kelly ready! Type 'exit' to quit.\n")
        
        # Run interactive UI
        client_ui.run()
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("  1. PDF files are in the ./data directory")
        print("  2. .env file exists with HUGGINGFACE_API_KEY\n")
        sys.exit(1)
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease check your .env file configuration.\n")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def demo_query(question: str):
    """
    Demo function to test with a single query.
    
    Args:
        question: Question to ask
    """
    config = Config()
    vector_store = initialize_loading_pipeline(config)
    retrieval_qa, client_ui = initialize_inference_pipeline(config, vector_store)
    
    # Ask single question
    client_ui.query_once(question)


if __name__ == "__main__":
    main()
