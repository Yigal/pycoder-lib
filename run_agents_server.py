#!/usr/bin/env python3
"""
Test script for the agents_server.py

This script starts the agents server in a separate process and tests all
available endpoints by sending requests and logging responses.
"""

import os
import sys
import time
import json
import logging
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server_test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("server_tester")

# Server configuration
SERVER_HOST = "localhost"
SERVER_PORT = 6003
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

def start_server() -> subprocess.Popen:
    """Start the agents server in a separate process.
    
    Returns:
        subprocess.Popen: Process handle for the server
    """
    logger.info("Starting agents server...")
    
    # Get the current script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Start the server
    server_process = subprocess.Popen(
        ["python", "agents_server.py"],
        cwd=str(script_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    logger.info("Waiting for server to start...")
    time.sleep(3)
    
    return server_process

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

def test_endpoint(method: str, endpoint: str, data: Dict[str, Any] = None, expected_status: int = 200) -> Dict[str, Any]:
    """Test a specific API endpoint.
    
    Args:
        method: HTTP method to use (get, post, delete)
        endpoint: API endpoint path
        data: Optional data to send
        expected_status: Expected HTTP status code
        
    Returns:
        Dict containing response data or empty dict on error
    """
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Testing {method.upper()} {endpoint}...")
    
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

def test_server():
    """Test all server endpoints."""
    try:
        # Test root endpoint
        root_response = test_endpoint("get", "/")
        
        # Test generate endpoint
        generate_data = {
            "prompt": "What's the capital of France?"
        }
        test_endpoint("post", "/generate", generate_data)
        
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
        agent_response = test_endpoint("post", "/agents", agent_data)
        agent_id = agent_response.get("agent_id")
        
        # If agent was created successfully, test run and delete
        if agent_id:
            # Test agents list endpoint
            test_endpoint("get", "/agents")
            
            # Test run agent endpoint
            run_data = {
                "prompt": "Tell me a short joke"
            }
            test_endpoint("post", f"/agents/{agent_id}/run", run_data)
            
            # Test delete agent endpoint
            test_endpoint("delete", f"/agents/{agent_id}")
            
            # Verify agent was deleted
            agents_list = test_endpoint("get", "/agents")
            agents = agents_list.get("agents", [])
            if not any(a.get("agent_id") == agent_id for a in agents):
                logger.info("Agent successfully deleted and removed from list")
            else:
                logger.error("Agent still in list after deletion")
                
        logger.info("All tests completed")
    except Exception as e:
        logger.error(f"Error testing server: {str(e)}")

def stop_server(server_process: subprocess.Popen):
    """Stop the server process.
    
    Args:
        server_process: Process handle for the server
    """
    logger.info("Stopping server...")
    
    # Try to terminate nicely
    server_process.terminate()
    
    # Wait for process to end (with timeout)
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        # Force kill if it doesn't terminate gracefully
        logger.warning("Server didn't terminate gracefully, force killing...")
        server_process.kill()
    
    # Log any output/errors from the server
    stdout, stderr = server_process.communicate()
    
    if stdout:
        logger.info(f"Server stdout: {stdout}")
    if stderr:
        logger.error(f"Server stderr: {stderr}")
    
    logger.info("Server stopped")

if __name__ == "__main__":
    # Start the server
    server_process = start_server()
    
    try:
        # Check if server is running
        if check_server_is_running():
            logger.info("Server is running")
            
            # Run all tests
            test_server()
        else:
            logger.error("Server failed to start")
            
            # Log server output/errors
            stdout, stderr = server_process.communicate()
            
            if stdout:
                logger.info(f"Server stdout: {stdout}")
            if stderr:
                logger.error(f"Server stderr: {stderr}")
    except Exception as e:
        logger.exception(f"Error during testing: {str(e)}")
    finally:
        # Always stop the server
        stop_server(server_process)
