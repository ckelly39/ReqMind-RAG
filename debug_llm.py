"""Debug script to test LLM connection"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from llm import HuggingFaceInferenceLLM

# Load config
config = Config()

print(f"API Key: {config.get_api_key()[:20]}...")
print(f"Model: {config.get_model_name()}")

# Initialize LLM
try:
    llm = HuggingFaceInferenceLLM(
        api_key=config.get_api_key(),
        model_name=config.get_model_name()
    )
    
    print("\n✓ LLM initialized successfully")
    
    # Test simple generation
    print("\n🔍 Testing text generation...")
    test_prompt = "Answer the following question: What is machine learning?"
    
    result = llm._call(test_prompt)
    print(f"\n✓ Generated response: {result}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
