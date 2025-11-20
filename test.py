import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

project_root = Path(__file__).resolve().parent
env_path = project_root / ".env"
if not env_path.exists():
    raise FileNotFoundError(f".env file not found at {env_path}")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("HUGGINGFACE_API_KEY")
model = os.getenv("TEST_CHAT_MODEL", "HuggingFaceH4/zephyr-7b-beta")

client = InferenceClient(model=model, token=api_key)

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    max_tokens=32,
    temperature=0.7,
)
choice = response.choices[0]
print("Model:", response.model)
print("Finish reason:", choice.finish_reason)
print("Reply:", choice.message["content"].strip())
