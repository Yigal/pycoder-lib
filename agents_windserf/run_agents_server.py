#!/usr/bin/env python3
"""
Server runner for the Agents Windserf package.

This script starts the agents server and optionally runs tests to verify functionality.
"""

import os
import sys
import time
import json
import logging
import requests
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Server configuration
SERVER_HOST = "localhost"
SERVER_PORT = 6003
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

def configure_logging(log_file=None):
    """Configure logging for the server runner.
    
    Args:
        log_file: Optional path to a log file
    """
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )
    return logging.getLogger("server_runner")

def check_server_is_running() -> bool:
    """Check if the server is running by calling the root endpoint.
    
    Returns:
        bool: True if server is running, False otherwise
    """
    try:
        response = requests.get(f"{BASE_URL}/")
        return response.status_code == 200
    except requests.RequestException:
        return False

def test_endpoint(logger, method: str, endpoint: str, data: Dict[str, Any] = None, expected_status: int = 200) -> Dict:
    """Test a specific API endpoint.
    
    Args:
        logger: Logger instance
        method: HTTP method to use (get, post, delete)
        endpoint: API endpoint path
        data: Optional data to send
        expected_status: Expected HTTP status code
        
    Returns:
        Dict containing response data or empty dict on error
    """
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Testing {method.upper()} {url}")
    
    if data:
        logger.info(f"Request data: {json.dumps(data, indent=2)}")
    
    try:
        if method.lower() == "get":
            response = requests.get(url)
        elif method.lower() == "post":
            response = requests.post(url, json=data)
        elif method.lower() == "delete":
            response = requests.delete(url)
        else:
            logger.error(f"Unsupported method: {method}")
            return {}
        
        if response.status_code == expected_status:
            response_data = response.json()
            logger.info(f"Response: {json.dumps(response_data, indent=2)}")
            return response_data
        else:
            logger.error(f"Error testing {endpoint}: {response.status_code} {response.reason}")
            return {}
    except Exception as e:
        logger.error(f"Exception testing {endpoint}: {str(e)}")
        return {}

def test_server(logger):
    """Test all server endpoints."""
    try:
        # Test root endpoint
        root_response = test_endpoint(logger, "get", "/")
        
        # Test generate endpoint
        generate_data = {
            "prompt": "What's the capital of France?"
        }
        test_endpoint(logger, "post", "/generate", generate_data)
        
        # Test create agent endpoint
        agent_data = {
            "name": "Test Agent",
            "provider": "anthropic",
            "model_name": "claude-3-haiku-20240307",
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }
        agent_response = test_endpoint(logger, "post", "/agents", agent_data)
        agent_id = agent_response.get("agent_id")
        
        # If agent was created successfully, test run and delete
        if agent_id:
            # Test agents list endpoint
            test_endpoint(logger, "get", "/agents")
            
            # Test run agent endpoint
            run_data = {
                "prompt": "Tell me a short joke"
            }
            test_endpoint(logger, "post", f"/agents/{agent_id}/run", run_data)
            
            # Test delete agent endpoint
            test_endpoint(logger, "delete", f"/agents/{agent_id}")
            
            # Verify agent was deleted
            agents_list = test_endpoint(logger, "get", "/agents")
            
        logger.info("All tests completed")
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")

def run_server(host="0.0.0.0", port=SERVER_PORT, reload=False):
    """Run the agents server directly."""
    from .agents_server import start_server
    start_server(host=host, port=port, reload=reload)

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Agents Windserf Server Runner")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=SERVER_PORT, help="Port to run the server on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--test", action="store_true", help="Run tests after starting the server")
    parser.add_argument("--log-file", help="Path to log file (optional)")
    
    args = parser.parse_args()
    
    # Configure logging
    logger = configure_logging(args.log_file)
    
    if args.test:
        # Import for testing only
        import threading
        import time
        
        # Start server in a thread
        server_thread = threading.Thread(
            target=run_server,
            kwargs={"host": args.host, "port": args.port, "reload": args.reload}
        )
        server_thread.daemon = True
        server_thread.start()
        
        # Wait for server to start
        logger.info("Waiting for server to start...")
        max_attempts = 10
        for i in range(max_attempts):
            if check_server_is_running():
                logger.info("Server is running")
                break
            logger.info(f"Attempt {i+1}/{max_attempts}: Server not ready yet")
            time.sleep(2)
        
        # Run tests
        if check_server_is_running():
            test_server(logger)
        else:
            logger.error("Server failed to start")
            sys.exit(1)
    else:
        # Just run the server
        logger.info(f"Starting server on {args.host}:{args.port}")
        run_server(host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
