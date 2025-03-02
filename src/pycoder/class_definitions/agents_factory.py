"""Agent factory module for the AgentsCrowd platform.

This module provides factory functions and classes for creating and running agents
with different models and providers.
"""

import json
import time
import logging
from typing import Any, Dict, Optional, Callable
from pathlib import Path

from pydantic import BaseModel

from .model_def import (
    AgentModel, 
    create_model,
    get_model_api_keys
)
from .results_type_def import AgentResult

# Configure basic logging
logger = logging.getLogger(__name__)

# Model cache to avoid creating duplicate models
model_cache: Dict[str, AgentModel] = {}


def get_model(provider: str, model_name: str, api_key: Optional[str] = None) -> AgentModel:
    """Get a model instance from the cache or create a new one.
    
    Args:
        provider: The provider of the model.
        model_name: The name of the model.
        api_key: The API key for the provider. If None, it will be taken from the configuration.
        
    Returns:
        AgentModel: An instance of the appropriate model class.
    """
    cache_key = f"{provider}/{model_name}/{api_key}"
    
    if cache_key not in model_cache:
        model_cache[cache_key] = create_model(provider, model_name, api_key)
    
    return model_cache[cache_key]


class Agent(BaseModel):
    """Model representing an agent.
    
    Attributes:
        name: The name of the agent.
        type: The type of the agent (e.g., "text_agent").
        provider: The provider of the model.
        model_name: The name of the model.
        api_key: The API key for the provider.
        parameters: Additional parameters for the agent.
    """
    
    name: str
    type: str
    provider: str
    model_name: str
    api_key: Optional[str] = None
    parameters: Dict[str, Any] = {}


class AgentRunner:
    """Runner for executing AI agents.
    
    Attributes:
        agent: The agent to run.
        model: The model to use for the agent.
        last_result: The last result of the agent.
        _running: Whether the agent is currently running.
        start_time: The time when the agent started running.
    """
    
    def __init__(self, agent: Agent) -> None:
        """Initialize the agent runner.
        
        Args:
            agent: The agent to run.
        """
        self.agent = agent
        self.model = get_model(agent.provider, agent.model_name, agent.api_key)
        self.last_result: Optional[AgentResult] = None
        self._running: bool = False
        self.start_time: Optional[float] = None
    
    def run(self, prompt: str, **kwargs: Any) -> AgentResult:
        """Run the agent with the given prompt.
        
        Args:
            prompt: The prompt to use for the agent.
            **kwargs: Additional arguments for the model.
            
        Returns:
            AgentResult: The result of the agent run.
        """
        # Merge parameters from agent with kwargs
        params = {**self.agent.parameters, **kwargs}
        
        logger.info(f"Running agent {self.agent.name} with model {self.model.get_full_name()}")
        
        # Mark the agent as running
        self._running = True
        self.start_time = time.time()
        
        try:
            # Generate content
            content = self.model.generate(prompt, **params)
            
            # Create and store result
            result = AgentResult(
                content=content,
                model=self.model.get_full_name(),
                timestamp=time.time(),
                prompt=prompt
            )
            
            self.last_result = result
            return result
        finally:
            # Mark the agent as not running
            self._running = False
    
    def is_running(self) -> bool:
        """Check if the agent is currently running.
        
        Returns:
            bool: True if the agent is running, False otherwise.
        """
        return self._running
    
    def set_model(self, provider: str, model_name: str, api_key: Optional[str] = None) -> None:
        """Set a new model for the agent.
        
        Args:
            provider: The provider of the model.
            model_name: The name of the model.
            api_key: The API key for the provider. If None, it will be taken from the configuration.
        """
        self.model = get_model(provider, model_name, api_key)
        self.agent.provider = provider
        self.agent.model_name = model_name
        self.agent.api_key = api_key
    
    def save_result(self, path: str) -> None:
        """Save the last result to a file.
        
        Args:
            path: The path to save the result to.
            
        Raises:
            ValueError: If there is no last result.
        """
        if self.last_result is None:
            raise ValueError("No result to save")
        
        with open(path, "w") as f:
            f.write(json.dumps(self.last_result.model_dump(), indent=2))
    
    def get_last_result(self) -> Optional[AgentResult]:
        """Get the last result of the agent.
        
        Returns:
            Optional[AgentResult]: The last result of the agent, or None if there is no last result.
        """
        return self.last_result
