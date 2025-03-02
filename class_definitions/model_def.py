"""Model definitions for the AgentsCrowd platform.

This module defines the model classes used by agents to generate content
with different AI providers.
"""

import logging
import os
from typing import Any, Dict, Optional
import importlib.util

# Configure basic logging
logger = logging.getLogger(__name__)

# Optional imports with fallbacks
try:
    import anthropic
except ImportError:
    anthropic = None
    logger.warning("anthropic module not found. AnthropicModel will not be fully functional.")

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    logger.warning("google.generativeai module not found. GeminiModel will not be fully functional.")

try:
    import openai
except ImportError:
    openai = None
    logger.warning("openai module not found. OpenAIModel will not be fully functional.")

try:
    import requests
except ImportError:
    requests = None
    logger.warning("requests module not found. GroqModel and OpenRouterModel will not be fully functional.")


# Simple implementation to get model API keys if needed
def get_model_api_keys() -> Dict[str, Optional[str]]:
    """
    Get API keys for various LLM providers from environment variables.
    
    Returns:
        Dict[str, Optional[str]]: A dictionary mapping provider names to API keys.
    """
    return {
        "openai": os.getenv("OPENAI_API_KEY"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "gemini": os.getenv("GEMINI_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
    }


class AgentModel:
    """Base class for all agent models.
    
    Attributes:
        name: The name of the model.
        provider: The provider of the model.
    """
    
    def __init__(self, name: str, provider: str) -> None:
        """Initialize the agent model.
        
        Args:
            name: The name of the model.
            provider: The provider of the model.
        """
        self.name = name
        self.provider = provider
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using the model.
        
        Args:
            prompt: The prompt to use for generation.
            **kwargs: Additional arguments for the model.
            
        Returns:
            str: The generated content.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement generate()")
    
    def get_full_name(self) -> str:
        """Get the full name of the model.
        
        Returns:
            str: A string in the format "provider/name".
        """
        return f"{self.provider}/{self.name}"


class OpenAIModel(AgentModel):
    """Model implementation for OpenAI API.
    
    Attributes:
        name: The name of the model.
        provider: The provider of the model, always "openai".
        api_key: The API key for OpenAI.
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        """Initialize the OpenAI model.
        
        Args:
            name: The name of the model (e.g., "gpt-4").
            api_key: The API key for OpenAI. If None, it will be taken from the configuration.
        """
        super().__init__(name, "openai")
        self.api_key = api_key or get_model_api_keys()["openai"]
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using the OpenAI model.
        
        Args:
            prompt: The prompt to use for generation.
            **kwargs: Additional arguments for the OpenAI API.
            
        Returns:
            str: The generated content.
            
        Raises:
            Exception: If the API call fails.
        """
        if openai is None:
            raise ImportError("openai module is required for OpenAIModel")
            
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.name,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating content with OpenAI model {self.name}: {str(e)}")
            raise


class AnthropicModel(AgentModel):
    """Model implementation for Anthropic API.
    
    Attributes:
        name: The name of the model.
        provider: The provider of the model, always "anthropic".
        api_key: The API key for Anthropic.
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        """Initialize the Anthropic model.
        
        Args:
            name: The name of the model (e.g., "claude-3-opus-20240229").
            api_key: The API key for Anthropic. If None, it will be taken from the configuration.
        """
        super().__init__(name, "anthropic")
        self.api_key = api_key or get_model_api_keys()["anthropic"]
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using the Anthropic model.
        
        Args:
            prompt: The prompt to use for generation.
            **kwargs: Additional arguments for the Anthropic API.
            
        Returns:
            str: The generated content.
            
        Raises:
            Exception: If the API call fails.
        """
        if anthropic is None:
            raise ImportError("anthropic module is required for AnthropicModel")
            
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.name,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error generating content with Anthropic model {self.name}: {str(e)}")
            raise


class GeminiModel(AgentModel):
    """Model implementation for Google Gemini API.
    
    Attributes:
        name: The name of the model.
        provider: The provider of the model, always "gemini".
        api_key: The API key for Gemini.
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        """Initialize the Gemini model.
        
        Args:
            name: The name of the model (e.g., "gemini-pro").
            api_key: The API key for Gemini. If None, it will be taken from the configuration.
        """
        super().__init__(name, "gemini")
        self.api_key = api_key or get_model_api_keys()["gemini"]
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Configure the Gemini API if available
        if genai is not None:
            genai.configure(api_key=self.api_key)
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using the Gemini model.
        
        Args:
            prompt: The prompt to use for generation.
            **kwargs: Additional arguments for the Gemini API.
            
        Returns:
            str: The generated content.
            
        Raises:
            Exception: If the API call fails.
        """
        if genai is None:
            raise ImportError("google.generativeai module is required for GeminiModel")
            
        try:
            model = genai.GenerativeModel(self.name)
            response = model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            logger.error(f"Error generating content with Gemini model {self.name}: {str(e)}")
            raise


class GroqModel(AgentModel):
    """Model implementation for Groq API.
    
    Attributes:
        name: The name of the model.
        provider: The provider of the model, always "groq".
        api_key: The API key for Groq.
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        """Initialize the Groq model.
        
        Args:
            name: The name of the model (e.g., "llama3-70b-8192").
            api_key: The API key for Groq. If None, it will be taken from the configuration.
        """
        super().__init__(name, "groq")
        self.api_key = api_key or get_model_api_keys()["groq"]
        if not self.api_key:
            raise ValueError("Groq API key is required")
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using the Groq model.
        
        Args:
            prompt: The prompt to use for generation.
            **kwargs: Additional arguments for the Groq API.
            
        Returns:
            str: The generated content.
            
        Raises:
            Exception: If the API call fails.
        """
        if requests is None:
            raise ImportError("requests module is required for GroqModel")
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.name,
                "messages": [{"role": "user", "content": prompt}],
                **kwargs
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating content with Groq model {self.name}: {str(e)}")
            raise


class OpenRouterModel(AgentModel):
    """Model implementation for OpenRouter API.
    
    Attributes:
        name: The name of the model.
        provider: The provider of the model, always "openrouter".
        api_key: The API key for OpenRouter.
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        """Initialize the OpenRouter model.
        
        Args:
            name: The name of the model (e.g., "anthropic/claude-3-opus-20240229").
            api_key: The API key for OpenRouter. If None, it will be taken from the configuration.
        """
        super().__init__(name, "openrouter")
        self.api_key = api_key or get_model_api_keys()["openrouter"]
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using the OpenRouter model.
        
        Args:
            prompt: The prompt to use for generation.
            **kwargs: Additional arguments for the OpenRouter API.
            
        Returns:
            str: The generated content.
            
        Raises:
            Exception: If the API call fails.
        """
        if requests is None:
            raise ImportError("requests module is required for OpenRouterModel")
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.name,
                "messages": [{"role": "user", "content": prompt}],
                **kwargs
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating content with OpenRouter model {self.name}: {str(e)}")
            raise


def create_model(provider: str, model_name: str, api_key: Optional[str] = None) -> AgentModel:
    """Create a model instance based on the provider and model name.
    
    Args:
        provider: The provider of the model.
        model_name: The name of the model.
        api_key: The API key for the provider. If None, it will be taken from the configuration.
        
    Returns:
        AgentModel: An instance of the appropriate model class.
        
    Raises:
        ValueError: If the provider is not supported.
        ImportError: If the dependencies for the provider are not available.
    """
    provider = provider.lower()
    
    # Check if provider is supported
    if provider == "openai":
        if openai is None:
            raise ImportError("The 'openai' package is required for using OpenAI models.")
        return OpenAIModel(model_name, api_key)
    elif provider == "anthropic":
        if anthropic is None:
            raise ImportError("The 'anthropic' package is required for using Anthropic models.")
        return AnthropicModel(model_name, api_key)
    elif provider == "gemini":
        if genai is None:
            raise ImportError("The 'google.generativeai' package is required for using Gemini models.")
        return GeminiModel(model_name, api_key)
    elif provider == "groq":
        if requests is None:
            raise ImportError("The 'requests' package is required for using Groq models.")
        return GroqModel(model_name, api_key)
    elif provider == "openrouter":
        if requests is None:
            raise ImportError("The 'requests' package is required for using OpenRouter models.")
        return OpenRouterModel(model_name, api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
