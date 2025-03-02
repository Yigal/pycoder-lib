#!/usr/bin/env python3
"""
Simple script to interact with the agent server.

This script demonstrates how to query the agent server for a list of available agents.
"""

import sys
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


def list_agents() -> None:
    """
    Query the agent server and list all available agents.
    
    This function makes a GET request to the /agents endpoint and displays
    the results in a formatted way.
    """
    server_url = "http://localhost:6001"
    endpoint = "/agents"
    
    try:
        # Make the request to the agent server
        response = requests.get(f"{server_url}{endpoint}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the response contains agents
        if "agents" not in data or not data["agents"]:
            print("No agents found on the server.")
            return
        
        # Display the agents in a formatted way
        print("\n===== Available Agents =====")
        print(f"Total agents: {len(data['agents'])}\n")
        
        for idx, agent in enumerate(data["agents"], 1):
            print(f"Agent {idx}:")
            print(f"  ID: {agent.get('id', 'N/A')}")
            print(f"  Name: {agent.get('name', 'N/A')}")
            print(f"  Provider: {agent.get('provider', 'N/A')}")
            print(f"  Model: {agent.get('model', 'N/A')}")
            
            # Format created_at timestamp if available
            created_at = agent.get('created_at')
            if created_at:
                created_time = datetime.fromtimestamp(created_at)
                print(f"  Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("  Created: Built-in agent")
            
            print()  # Empty line between agents
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the agent server. Is it running?")
        print(f"Attempted to connect to: {server_url}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Received invalid JSON response from the server.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("Querying agent server for available agents...\n")
    list_agents()
