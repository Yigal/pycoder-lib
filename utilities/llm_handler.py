"""LLM handler utilities for interacting with different model providers."""

from typing import Dict, Any, Optional
from datetime import datetime

def create_llm_config(
    name: str,
    provider: str,
    model_name: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a configuration for an LLM agent.
    
    Args:
        name: Name of the agent configuration
        provider: Provider name (e.g., 'anthropic', 'openai')
        model_name: Name of the model to use
        parameters: Model parameters like temperature, max_tokens
        
    Returns:
        Dict containing the complete LLM configuration
    """
    return {
        "name": name,
        "type": "chat",
        "provider": provider,
        "model_name": model_name,
        "parameters": parameters
    }

def generate_llm_response(
    model: Any,
    prompt: str,
    system_message: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """Generate a response from an LLM model.
    
    Args:
        model: The LLM model instance
        prompt: Input prompt for generation
        system_message: Optional system message
        **kwargs: Additional model parameters
        
    Returns:
        Dict containing the response content and metadata
    """
    # For testing with mock API keys, return a mock response
    if hasattr(model, 'agent') and hasattr(model.agent, 'provider'):
        provider = model.agent.provider
        model_name = model.agent.model_name
    else:
        provider = getattr(model, 'provider', 'unknown')
        model_name = getattr(model, 'model_name', 'unknown')
        
    if provider == "mock" or "mock" in str(model_name).lower():
        content = f"This is a mock response for the prompt: {prompt[:50]}..."
    else:
        # Call the actual model's generate method
        try:
            content = model.run(prompt) if hasattr(model, 'run') else model.generate(prompt, system_message, **kwargs)
            if hasattr(content, 'content'):
                content = content.content
        except Exception as e:
            # Propagate the error instead of returning a mock response
            raise
    
    return {
        "content": content,
        "model": f"{provider}/{model_name}",
        "timestamp": datetime.now().timestamp()
    }

def validate_model_config(config: Dict[str, Any]) -> bool:
    """Validate an LLM model configuration.
    
    Args:
        config: The model configuration to validate
        
    Returns:
        bool: True if configuration is valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_fields = ["name", "type", "provider", "model_name", "parameters"]
    if not all(field in config for field in required_fields):
        raise ValueError(f"Missing required fields. Required: {required_fields}")
    
    if not isinstance(config["parameters"], dict):
        raise ValueError("Parameters must be a dictionary")
        
    return True
