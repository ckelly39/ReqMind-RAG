"""
Inference Client Component (Adapter Pattern)
Wraps HuggingFace Inference API with a clean interface.
"""

from typing import Dict, Any

import requests
from huggingface_hub import InferenceClient as HFInferenceClient

# huggingface_hub relocated several errors in recent releases,
# so we try the modern location first and fall back for older versions.
try:  # huggingface_hub >= 0.24
    from huggingface_hub.errors import HfHubHTTPError, InferenceTimeoutError
except ImportError:  # Older huggingface_hub kept them under utils
    from huggingface_hub.utils import HfHubHTTPError, InferenceTimeoutError


class InferenceClient:
    """
    Adapter for HuggingFace Inference API.
    Provides clean interface and handles HTTP communication, authentication, and errors.
    """

    def __init__(self, api_key: str, model_name: str):
        """
        Initialize inference client.

        Args:
            api_key: HuggingFace API key
            model_name: Model identifier (e.g., "mistralai/Mistral-7B-Instruct-v0.3")
        """
        self.api_key = api_key
        self.model_name = model_name
        # Keep the URL for logging even though the SDK handles routing.
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{model_name}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.client = HFInferenceClient(model=model_name, token=api_key)

        print(f"[OK] InferenceClient initialized for model: {model_name}")
        print(f"      Using endpoint: {self.api_url}\n")

    def text_generation(
        self,
        prompt: str,
        max_new_tokens: int = 500,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repetition_penalty: float = 1.1,
    ) -> str:
        """
        Generate text from prompt using HuggingFace Inference API.

        Args:
            prompt: Input prompt for generation
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            repetition_penalty: Penalty for repetition

        Returns:
            Generated text string

        Raises:
            ValueError: If response format is invalid or API call fails
        """
        try:
            # Try chat_completion first (for newer models like Mistral, Zephyr, etc.)
            try:
                messages = [{"role": "user", "content": prompt}]
                result = self.client.chat_completion(
                    messages=messages,
                    max_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                )
                # Extract the generated text from chat completion response
                if hasattr(result, 'choices') and len(result.choices) > 0:
                    return result.choices[0].message.content.strip()
                elif isinstance(result, dict) and 'choices' in result:
                    return result['choices'][0]['message']['content'].strip()
                else:
                    raise ValueError(f"Unexpected chat completion format: {result}")
            except (AttributeError, ValueError) as chat_err:
                # Fall back to text_generation if chat_completion fails
                result = self.client.text_generation(
                    prompt,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty,
                    return_full_text=False,
                )
                if isinstance(result, str):
                    return result.strip()
                if isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"].strip()
                raise ValueError(f"Unexpected response format: {result}")
                
        except InferenceTimeoutError as exc:
            raise TimeoutError(
                f"Request to {self.model_name} timed out after 30 seconds. "
                "The model may be loading or experiencing high demand."
            ) from exc
        except HfHubHTTPError as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            if status_code == 401:
                raise ValueError("Invalid API key. Check your HUGGINGFACE_API_KEY.") from exc
            if status_code == 404:
                raise ValueError(
                    f"Model {self.model_name} not found. "
                    "Please check the model name in your .env file."
                ) from exc
            if status_code == 410:
                raise ValueError(
                    f"Model {self.model_name} is no longer available (410 Gone). "
                    "Please use a different model (e.g., mistralai/Mistral-7B-Instruct-v0.3)"
                ) from exc
            if status_code == 429:
                raise ValueError("Rate limit exceeded. Please wait and try again.") from exc
            if status_code == 503:
                raise ValueError(
                    f"Model {self.model_name} is currently loading. "
                    "Please wait a minute and try again."
                ) from exc
            raise ValueError(f"API request failed: {exc}") from exc

    def authenticate(self) -> bool:
        """
        Test API authentication.

        Returns:
            True if authentication successful

        Raises:
            ValueError: If authentication fails
        """
        try:
            response = requests.get(
                f"https://huggingface.co/api/models/{self.model_name}",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return True
        except requests.HTTPError as exc:
            raise ValueError("Authentication failed. Check your API key.") from exc

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model.

        Returns:
            Dictionary with model information
        """
        response = requests.get(
            f"https://huggingface.co/api/models/{self.model_name}",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
