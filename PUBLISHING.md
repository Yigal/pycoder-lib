---
noteId: "2be3e2c0f76411ef9dfee764c100c7f9"
tags: []

---

# Publishing the PyCoder Package

This document explains how to use the `publish_package.py` script to build and publish the PyCoder package to PyPI.

## Prerequisites

1. You need a PyPI account (register at [pypi.org](https://pypi.org/account/register/))
2. You may also want a TestPyPI account (register at [test.pypi.org](https://test.pypi.org/account/register/))

## Usage

The `publish_package.py` script automates the process of building and publishing your package. You can run it with different options:

```bash
# Basic usage (interactive)
./publish_package.py

# Skip uploading to TestPyPI and go straight to PyPI
./publish_package.py --skip-test-pypi

# Skip uploading to PyPI (only build and upload to TestPyPI)
./publish_package.py --skip-pypi

# Provide username on the command line
./publish_package.py --username your_username

# Skip local installation test
./publish_package.py --skip-local-install
```

## Steps Performed by the Script

1. Cleans previous build artifacts
2. Installs or upgrades necessary build tools
3. Builds the package distributions
4. Optionally installs the package locally for testing
5. Uploads to TestPyPI (optional)
6. Uploads to PyPI (optional)

## Manual Testing After Publishing

After publishing to TestPyPI, you can install and test the package with:

```bash
pip install --index-url https://test.pypi.org/simple/ pycoder
```

After publishing to PyPI, users can install the package with:

```bash
pip install pycoder
```

## Versioning

Remember to update the version number in `pyproject.toml` before publishing a new release.

## Troubleshooting

- If you get an error about a package name already being taken, you'll need to choose a different name in your `pyproject.toml` file.
- If you get authentication errors, double-check your PyPI username and password.
- For other issues, check the [PyPI Help](https://pypi.org/help/) documentation.
