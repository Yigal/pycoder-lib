"""Agent management utilities for creating and managing agent instances."""

from typing import Dict, Any, Optional, List
from uuid import uuid4
from datetime import datetime

def create_agent_id(name: str) -> str:
    """Generate a unique agent ID.
    
    Args:
        name: Base name for the agent
        
    Returns:
        str: Unique agent identifier
    """
    return f"{name.lower().replace(' ', '_')}_{str(uuid4())[:8]}"

def store_agent(
    agent_store: Dict[str, Any],
    agent: Any,
    agent_id: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Store an agent instance with its configuration.
    
    Args:
        agent_store: Dictionary storing agent instances
        agent: Agent instance to store
        agent_id: Unique identifier for the agent
        config: Agent configuration
        
    Returns:
        Dict containing agent creation response
    """
    agent_store[agent_id] = {
        "agent": agent,
        "config": config,
        "creation_time": datetime.now().timestamp()
    }
    
    return {
        "agent_id": agent_id,
        "name": config["name"],
        "status": "created"
    }

def list_stored_agents(agent_store: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List all stored agents and their configurations.
    
    Args:
        agent_store: Dictionary storing agent instances
        
    Returns:
        List of agent information dictionaries
    """
    return [
        {
            "agent_id": agent_id,
            "name": info["config"]["name"],
            "provider": info["config"]["provider"],
            "model": info["config"]["model_name"],
            "creation_time": info["config"].get("creation_time", info.get("creation_time"))
        }
        for agent_id, info in agent_store.items()
    ]

def get_agent_info(
    agent_store: Dict[str, Any],
    agent_id: str
) -> Optional[Dict[str, Any]]:
    """Retrieve agent information by ID.
    
    Args:
        agent_store: Dictionary storing agent instances
        agent_id: ID of the agent to retrieve
        
    Returns:
        Dict containing agent information or None if not found
    """
    if agent_id not in agent_store:
        return None
        
    info = agent_store[agent_id]
    return {
        "agent_id": agent_id,
        "name": info["config"]["name"],
        "provider": info["config"]["provider"],
        "model": info["config"]["model_name"],
        "creation_time": info["config"].get("creation_time", info.get("creation_time"))
    }

def remove_agent(
    agent_store: Dict[str, Any],
    agent_id: str
) -> bool:
    """Remove an agent from storage.
    
    Args:
        agent_store: Dictionary storing agent instances
        agent_id: ID of the agent to remove
        
    Returns:
        bool: True if agent was removed, False if not found
    """
    if agent_id in agent_store:
        del agent_store[agent_id]
        return True
    return False
