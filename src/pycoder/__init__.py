"""
PyCoder: A flexible AI agent management system with support for multiple LLM providers.

This package provides a framework for creating, managing, and running AI agents
with different LLM providers including OpenAI, Anthropic, Gemini, Groq, and OpenRouter.
"""

__version__ = "0.1.0"

# Re-export commonly used components
from .agents import Agent, AgentRunner
from .class_definitions.model_def import get_model_api_keys
from .class_definitions.results_type_def import AgentResult

# Convenience functions
from .utilities.runtime_handler import setup_runtime_environment
