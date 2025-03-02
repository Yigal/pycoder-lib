"""Tool definitions for the AgentsCrowd platform.

This module defines the tools used by agents to perform specific tasks.
The current version provides a base structure for future tool implementations.
"""

from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union

# Define a type variable for function return values
T = TypeVar('T')


class ToolContext:
    """Context for tool execution.
    
    Attributes:
        agent_name: Name of the agent executing the tool.
        model_name: Name of the model being used.
        parameters: Additional parameters for tool execution.
    """
    
    def __init__(
        self, 
        agent_name: str, 
        model_name: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize the tool context.
        
        Args:
            agent_name: Name of the agent executing the tool.
            model_name: Name of the model being used.
            parameters: Additional parameters for tool execution.
        """
        self.agent_name = agent_name
        self.model_name = model_name
        self.parameters = parameters or {}


class Tool:
    """Base class for agent tools.
    
    Attributes:
        name: The name of the tool.
        description: A description of what the tool does.
        function: The function to call when the tool is executed.
    """
    
    def __init__(
        self, 
        name: str, 
        description: str, 
        function: Callable[..., T]
    ) -> None:
        """Initialize the tool.
        
        Args:
            name: The name of the tool.
            description: A description of what the tool does.
            function: The function to call when the tool is executed.
        """
        self.name = name
        self.description = description
        self.function = function
    
    def execute(self, context: ToolContext, **kwargs: Any) -> T:
        """Execute the tool function.
        
        Args:
            context: The context for tool execution.
            **kwargs: Additional arguments for the tool function.
            
        Returns:
            The result of the tool function.
        """
        return self.function(context, **kwargs)


class ToolRegistry:
    """Registry for agent tools.
    
    Attributes:
        tools: Dictionary mapping tool names to Tool instances.
    """
    
    def __init__(self) -> None:
        """Initialize the tool registry."""
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool.
        
        Args:
            tool: The tool to register.
            
        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if tool.name in self.tools:
            raise ValueError(f"A tool with name '{tool.name}' is already registered")
        
        self.tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name.
        
        Args:
            name: The name of the tool to get.
            
        Returns:
            The tool if found, None otherwise.
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all registered tools.
        
        Returns:
            A list of dictionaries containing tool names and descriptions.
        """
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]


# Create a global tool registry
global_tool_registry = ToolRegistry()


def register_tool(
    name: str, 
    description: str
) -> Callable[[Callable[..., T]], Tool]:
    """Decorator to register a function as a tool.
    
    Args:
        name: The name of the tool.
        description: A description of what the tool does.
        
    Returns:
        A decorator function.
    """
    def decorator(func: Callable[..., T]) -> Tool:
        tool = Tool(name, description, func)
        global_tool_registry.register(tool)
        return tool
    
    return decorator
