"""Agent module for the PyCoder package.

This module provides functionality for creating and running AI agents
with different models and providers by re-exporting classes from
the class_definitions package.
"""

import logging
from pathlib import Path
from dotenv import load_dotenv

# Re-export from the class_definitions package
from .class_definitions import (
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

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if not already loaded
def load_env_vars(env_path=None):
    """Load environment variables from .env file if it exists"""
    if env_path is None:
        env_path = Path('.env')
    load_dotenv(dotenv_path=env_path if env_path.exists() else None)
