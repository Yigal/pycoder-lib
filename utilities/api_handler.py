"""API utilities for handling HTTP requests and responses."""

from typing import Dict, Any, Optional, Union, List
from fastapi import HTTPException
from pydantic import BaseModel

def create_error_response(
    status_code: int,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized error response.
    
    Args:
        status_code: HTTP status code
        message: Error message
        details: Optional error details
        
    Returns:
        HTTPException with formatted error content
    """
    content = {"error": message}
    if details:
        content["details"] = details
    return HTTPException(status_code=status_code, detail=content)

def validate_request_data(
    data: Dict[str, Any],
    required_fields: List[str]
) -> None:
    """Validate request data contains required fields.
    
    Args:
        data: Request data to validate
        required_fields: List of required field names
        
    Raises:
        HTTPException: If validation fails
    """
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise create_error_response(
            400,
            "Missing required fields",
            {"missing_fields": missing}
        )

def format_response(
    data: Union[Dict[str, Any], BaseModel],
    success: bool = True,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """Format a response with standardized structure.
    
    Args:
        data: Response data
        success: Whether the response indicates success
        message: Optional message
        
    Returns:
        Dict containing formatted response
    """
    response = {"data": data, "success": success}
    if message:
        response["message"] = message
    
    # Remove sensitive fields if data is a dict
    if isinstance(data, dict):
        sensitive_fields = ["api_key", "secret", "password", "token"]
        for k in sensitive_fields:
            if k in data:
                data[k] = "**redacted**"
                
    return response
