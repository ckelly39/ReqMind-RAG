"""
Custom LLM Component
Custom LangChain LLM implementation using InferenceClient.
Integrates HuggingFace Inference API with LangChain's LLM interface.
"""

from typing import Any, List, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

# Handle both direct run and module import
try:
    from .inference_client import InferenceClient
except ImportError:
    from inference_client import InferenceClient


class HuggingFaceInferenceLLM(LLM):
    """
    Custom LangChain LLM that uses InferenceClient for HuggingFace API.
    Wraps the Adapter pattern InferenceClient to work with LangChain chains.
    """
    
    client: InferenceClient
    max_new_tokens: int = 300
    temperature: float = 0.5
    top_p: float = 0.9
    repetition_penalty: float = 1.2
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        """
        Initialize custom LLM with InferenceClient.
        
        Args:
            api_key: HuggingFace API key
            model_name: Model identifier
            **kwargs: Additional parameters
        """
        # Initialize InferenceClient (Adapter pattern)
        client = InferenceClient(api_key=api_key, model_name=model_name)
        
        # Call parent constructor with client
        super().__init__(client=client, **kwargs)
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "huggingface_inference"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Call the LLM with a prompt.
        
        Args:
            prompt: Input prompt
            stop: Stop sequences (not implemented)
            run_manager: Callback manager
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        # Use InferenceClient to generate text
        try:
            response = self.client.text_generation(
                prompt=prompt,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                repetition_penalty=self.repetition_penalty
            )
            
            # Apply stop sequences to truncate response
            if stop:
                for stop_seq in stop:
                    if stop_seq in response:
                        response = response.split(stop_seq)[0]
            
            # Always stop at common question patterns
            stop_patterns = ["\n\nQuestion:", "\nQuestion:", "\n\nProvide", "------"]
            for pattern in stop_patterns:
                if pattern in response:
                    response = response.split(pattern)[0]
            
            return response.strip()
        except Exception as e:
            # Re-raise with more context
            raise ValueError(f"LLM generation failed: {e}")
    
    @property
    def _identifying_params(self) -> dict:
        """
        Get identifying parameters.
        Used by LangChain for caching and logging.
        """
        return {
            "model_name": self.client.model_name,
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "repetition_penalty": self.repetition_penalty
        }
    
    def get_model_name(self) -> str:
        """Get the model name."""
        return self.client.model_name
