"""
AgentsCrowd platform package.

This package provides functionality for creating and running AI agents
with different models and providers.
"""

# Re-export from agents.py
from .agents import (
    # Model definitions
    AgentModel,
    OpenAIModel,
    AnthropicModel,
    GeminiModel,
    GroqModel,
    OpenRouterModel,
    create_model,
    get_model_api_keys,
    
    # Result type definitions
    AgentResult,
    
    # Tool definitions
    Tool,
    ToolContext,
    ToolRegistry,
    register_tool,
    global_tool_registry,
    
    # Agent factory
    Agent,
    AgentRunner,
    get_model
)

__all__ = [
    # Model definitions
    'AgentModel',
    'OpenAIModel',
    'AnthropicModel',
    'GeminiModel',
    'GroqModel',
    'OpenRouterModel',
    'create_model',
    'get_model_api_keys',
    
    # Result type definitions
    'AgentResult',
    
    # Tool definitions
    'Tool',
    'ToolContext',
    'ToolRegistry',
    'register_tool',
    'global_tool_registry',
    
    # Agent factory
    'Agent',
    'AgentRunner',
    'get_model'
] 