---
noteId: "d50de8a0f76911ef9dfee764c100c7f9"
tags: []

---

# Publishing PyCoder to the World

This document describes how to use the `.helper_scripts/publish.py` script to publish PyCoder, making it available to everyone.

## Overview

The `.helper_scripts/publish.py` script automates the entire process of making PyCoder available to the public, including:

1. Package building and validation
2. Local testing
3. TestPyPI publication (optional)
4. PyPI publication (optional)
5. GitHub repository setup (optional)

## Prerequisites

- Python 3.7 or higher
- PyPI account (if publishing to PyPI)
- GitHub account (if setting up GitHub repository)
- GitHub CLI (optional, for easier GitHub repository setup)

## Environment Setup

Create a `.env` file with the following credentials (or they will be prompted during execution):

```
PYPI_USERNAME=your_username
PYPI_PASSWORD=your_password
GITHUB_ACCESS_TOKEN=your_github_token
```

These credentials will be used for publishing to PyPI and setting up the GitHub repository.

## Usage

Basic usage to run through the entire process:

```bash
python .helper_scripts/publish.py
```

### Command Line Options

- `--skip-test-pypi`: Skip uploading to TestPyPI
- `--skip-pypi`: Skip uploading to the main PyPI
- `--skip-github`: Skip GitHub repository setup
- `--skip-test-server`: Skip testing the server locally
- `--force`: Skip confirmations (use with caution)

### Examples

Publish to TestPyPI only (good for testing):
```bash
python .helper_scripts/publish.py --skip-pypi --skip-github
```

Publish directly to PyPI without testing on TestPyPI first:
```bash
python .helper_scripts/publish.py --skip-test-pypi
```

Setup GitHub repository only (no PyPI publishing):
```bash
python .helper_scripts/publish.py --skip-test-pypi --skip-pypi
```

## Workflow

The script follows this workflow:

1. Clean previous build artifacts
2. Install or upgrade build tools
3. Build the package
4. Install the package locally for testing
5. Test the server functionality
6. Upload to TestPyPI (if not skipped)
7. Verify TestPyPI package functionality
8. Upload to PyPI (if not skipped)
9. Setup GitHub repository (if not skipped)
10. Print summary and next steps

## Security Considerations

- Credentials are loaded from the `.env` file or prompted during execution
- Sensitive files like `.env` are not committed to the repository
- The script confirms important actions before proceeding

## Troubleshooting

If you encounter issues:

1. Make sure your PyPI username and password are correct
2. Verify that the package name 'pycoder' is available on PyPI
3. For GitHub repository issues, try creating the repository manually and then running the script with `--skip-github`
4. Check the error messages for specific information on what went wrong

## After Publication

After successfully publishing PyCoder, remember to:

1. Create comprehensive documentation
2. Set up continuous integration for future releases
3. Monitor for bug reports and feature requests
4. Establish a contribution workflow for community contributions
