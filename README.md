# PyCoder

A flexible AI agent management system with support for multiple LLM providers.

## Features

- **Multi-Provider Support**: Works with OpenAI, Anthropic, Gemini, Groq, and OpenRouter
- **Modular Design**: Easily extend to support additional LLM providers
- **FastAPI Integration**: High-performance API endpoints
- **Flexible Configuration**: Configure via environment variables or API parameters

## Installation

```bash
# Basic installation with minimal dependencies
pip install pycoder

# With specific provider support
pip install pycoder[openai]
pip install pycoder[anthropic]
pip install pycoder[gemini]
pip install pycoder[groq]
pip install pycoder[openrouter]

# With all providers
pip install pycoder[all]
```

## Usage

### Starting the Server

Option 1: Use the command-line entry point:

```bash
# Default - allows connections from any IP address (use for development or when you need external access)
pycoder

# Or specify host and port
pycoder --host 0.0.0.0 --port 8000

# Restrict to localhost only (more secure for local development)
pycoder --host 127.0.0.1 --port 8000
```

Option 2: Use the Python API:

```python
from pycoder.agents_server import start_server

# Start the server - allows connections from any IP address
start_server(host="0.0.0.0", port=8000)

# Restrict to localhost only
# start_server(host="127.0.0.1", port=8000)
```

### Environment Configuration

Create a `.env` file in your project root:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
OPENROUTER_API_KEY=your_openrouter_key
```

### API Endpoints

#### Create Chat Completion

```
POST /v1/chat/completions
```

Request Body:
```json
{
  "model": "gpt-4-turbo",
  "provider": "openai", 
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
}
```

Response:
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677858242,
  "model": "gpt-4-turbo",
  "provider": "openai",
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 7,
    "total_tokens": 20
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I assist you today?"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

## Development

### Setting up a development environment

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install development dependencies: `pip install -e ".[all]"`

### Running tests

```bash
python -m unittest discover tests
```

## License

MIT License
