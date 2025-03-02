#!/usr/bin/env python3
"""
Package publisher script for Agents Windserf.

This script automates the process of building and publishing the 
agents-windserf package to PyPI.
"""

import os
import sys
import shutil
import subprocess
import argparse
from getpass import getpass
from pathlib import Path
from dotenv import load_dotenv


def run_command(command, description=None, exit_on_error=True, env=None):
    """Run a shell command and print its output."""
    if description:
        print(f"\n=== {description} ===")
    
    print(f"Running: {' '.join(command)}")
    
    # Use provided env or current environment
    cmd_env = env if env is not None else os.environ.copy()
    
    result = subprocess.run(command, capture_output=True, text=True, env=cmd_env)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error output: {result.stderr}", file=sys.stderr)
    
    if exit_on_error and result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    
    return result


def clean_previous_builds():
    """Remove previous build artifacts."""
    print("\n=== Cleaning previous builds ===")
    dirs_to_remove = ['dist', 'build', 'agents_windserf.egg-info']
    
    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Removing {dir_path}")
            shutil.rmtree(dir_path)


def install_build_tools():
    """Install or upgrade required build tools."""
    run_command(
        ["pip", "install", "--upgrade", "pip", "build", "twine"],
        "Installing build tools"
    )


def build_package():
    """Build the package distribution files."""
    run_command(
        ["python", "-m", "build"],
        "Building package"
    )


def test_package_locally():
    """Install the package locally for testing."""
    result = run_command(
        ["pip", "install", "-e", "."],
        "Installing package locally for testing",
        exit_on_error=False
    )
    
    if result.returncode != 0:
        print("Warning: Local installation failed. You might want to check your package structure.")
        response = input("Continue with upload preparation? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)


def upload_to_test_pypi(username=None, password=None):
    """Upload the package to TestPyPI."""
    print("\n=== Uploading to TestPyPI ===")
    
    # Set environment variables for twine
    env = os.environ.copy()
    if username and password:
        env["TWINE_USERNAME"] = username
        env["TWINE_PASSWORD"] = password
        env["TWINE_REPOSITORY"] = "testpypi"
    
    upload_cmd = ["python", "-m", "twine", "upload", "--repository", "testpypi", "dist/*"]
    
    print(f"Running: {' '.join(upload_cmd)}")
    try:
        result = subprocess.run(upload_cmd, env=env, shell=True, text=True, capture_output=True)
        
        if result.returncode != 0:
            print(f"Error output: {result.stderr}")
            print(f"Standard output: {result.stdout}")
            print("\nFailed to upload to TestPyPI. You may need to:")
            print("1. Register on https://test.pypi.org/")
            print("2. Ensure you have correct credentials")
            print("3. Check if the package name is available")
        else:
            print("Successfully uploaded to TestPyPI!")
            print(f"View at: https://test.pypi.org/project/pycoder/")
            print("You can test the installation with:")
            print("pip install --index-url https://test.pypi.org/simple/ pycoder")
    except Exception as e:
        print(f"Exception occurred: {e}")
        print("\nFailed to upload to TestPyPI. You may need to:")
        print("1. Register on https://test.pypi.org/")
        print("2. Ensure you have correct credentials")
        print("3. Check if the package name is available")


def upload_to_pypi(username=None, password=None):
    """Upload the package to PyPI."""
    print("\n=== Uploading to PyPI ===")
    
    # Confirm before uploading to PyPI
    confirm = input("Are you sure you want to upload to PyPI? (y/n): ")
    if confirm.lower() != 'y':
        print("Skipping PyPI upload.")
        return
    
    # Set environment variables for twine
    env = os.environ.copy()
    if username and password:
        env["TWINE_USERNAME"] = username
        env["TWINE_PASSWORD"] = password
        env["TWINE_REPOSITORY"] = "pypi"
    
    upload_cmd = ["python", "-m", "twine", "upload", "dist/*"]
    
    print(f"Running: {' '.join(upload_cmd)}")
    try:
        result = subprocess.run(upload_cmd, env=env, shell=True, text=True, capture_output=True)
        
        if result.returncode != 0:
            print(f"Error output: {result.stderr}")
            print(f"Standard output: {result.stdout}")
            print("\nFailed to upload to PyPI. You may need to:")
            print("1. Register on https://pypi.org/")
            print("2. Ensure you have correct credentials")
            print("3. Check if the package name is available")
        else:
            print("Successfully uploaded to PyPI!")
            print(f"View at: https://pypi.org/project/pycoder/")
            print("Users can install it with: pip install pycoder")
    except Exception as e:
        print(f"Exception occurred: {e}")
        print("\nFailed to upload to PyPI. You may need to:")
        print("1. Register on https://pypi.org/")
        print("2. Ensure you have correct credentials")
        print("3. Check if the package name is available")


def load_credentials_from_env():
    """Load PyPI credentials from .env file if available."""
    # Load .env file
    load_dotenv()
    
    # Use PyPI-specific variable names to avoid conflicts with pip
    username = os.environ.get("PYPI_USERNAME")
    password = os.environ.get("PYPI_PASSWORD")
    
    return username, password


def main():
    """Main function to handle package publishing."""
    parser = argparse.ArgumentParser(description="Build and publish the agents-windserf package")
    parser.add_argument("--skip-test-pypi", action="store_true", help="Skip uploading to TestPyPI")
    parser.add_argument("--skip-pypi", action="store_true", help="Skip uploading to the main PyPI")
    parser.add_argument("--username", help="PyPI username (will look in .env as PYPI_USERNAME, then prompt if not found)")
    parser.add_argument("--skip-local-install", action="store_true", help="Skip local installation test")
    args = parser.parse_args()

    # Get credentials from .env or command line or prompt
    env_username, env_password = load_credentials_from_env()
    
    # Get credentials early
    if not args.skip_test_pypi or not args.skip_pypi:
        username = args.username or env_username or input("PyPI username: ")
        password = env_password or getpass("PyPI password: ")
        print(f"Using username: {username}")

    # Preparation steps
    clean_previous_builds()
    install_build_tools()
    build_package()
    
    # Optional local installation for testing
    if not args.skip_local_install:
        test_package_locally()
    
    # Upload to TestPyPI if not skipped
    if not args.skip_test_pypi:
        upload_to_test_pypi(username, password)
        
        # Ask if the TestPyPI package works before proceeding to PyPI
        if not args.skip_pypi:
            response = input("\nDid you verify the TestPyPI package works correctly? (y/n): ")
            if response.lower() != 'y':
                print("Exiting without uploading to PyPI. You can re-run with --skip-test-pypi when ready.")
                sys.exit(0)
    
    # Upload to PyPI if not skipped
    if not args.skip_pypi:
        upload_to_pypi(username, password)


if __name__ == "__main__":
    main()
