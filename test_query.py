"""Test ReqMind with a sample query"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from document_parser import DocumentParser
from text_splitter import TextSplitter
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from retrieval_component import RetrievalComponent
from llm import HuggingFaceInferenceLLM
from retrieval_qa import RetrievalQAComponent

# Load config
config = Config()

print("Loading vector store...")
embedding_generator = EmbeddingGenerator(model_name=config.get_embedding_model())
vector_store = VectorStore(
    embeddings=embedding_generator.embeddings,
    persist_directory=config.get_vector_db_path(),
    collection_name="reqmind_collection"
)
vector_store.load_existing()

print("Initializing retrieval and LLM...")
retrieval_component = RetrievalComponent(
    vector_store=vector_store,
    top_k=config.get_top_k()
)

llm = HuggingFaceInferenceLLM(
    api_key=config.get_api_key(),
    model_name=config.get_model_name()
)

qa_component = RetrievalQAComponent(
    llm=llm,
    retrieval_component=retrieval_component
)

print("\n" + "="*70)
print("Testing query...")
print("="*70)

query = "What are the authentication requirements?"
print(f"\nQuery: {query}\n")

result = qa_component.process_query(query)
print(f"Answer: {result['result']}\n")

if 'error' in result:
    print(f"ERROR: {result['error']}")
