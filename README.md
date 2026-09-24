# pyjsonparser

[![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://alexprodan99.github.io/pyjsonparser/)

A custom JSON parser implementation written in Python, featuring a lexer-parser architecture for robust JSON parsing and serialization.

## Overview

`pyjsonparser` is a lightweight JSON parser that implements the complete JSON specification. It includes:
- **Lexer**: Tokenizes JSON input strings
- **Parser**: Builds Python objects from tokens
- **Serializer**: Converts Python objects back to JSON strings

## Features

- Parse JSON strings into Python objects (dictionaries, lists, strings, numbers, booleans, null)
- Serialize Python objects back to JSON format
- Clean separation of concerns with abstract contracts and concrete implementations
- Comprehensive test coverage with pytest

## Requirements

- Python >= 3.12

## Installation

You can install `pyjsonparser` in two ways:

1. **Using pip**:
    ```bash
    pip install pyjsonparser
    ```

2. **Cloning the repository**:
    ```bash
    git clone <repository-url>
    cd pyjsonparser
    ```

    Install dependencies:
    ```bash
    poetry install
    ```

## Usage

```python
from pyjson import JsonParser

parser = JsonParser()

# Parse JSON string
json_object = parser.from_string('{"name": "John", "age": 30}')
# Result: {'name': 'John', 'age': 30}

# Convert to JSON string
json_string = parser.to_string({"name": "John", "age": 30})
# Result: '{"name": "John", "age": 30}'
```

## Documentation

The full documentation is hosted online at **[alexprodan99.github.io/pyjsonparser](https://alexprodan99.github.io/pyjsonparser/)**.

You can also browse the documentation source files directly in the [`docs/`](docs/) directory:

- [Getting Started](docs/getting-started.md)
- [Architecture & Design](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Usage Examples & Recipes](docs/examples.md)
- [Contributing & Development Guide](docs/contributing.md)

## Project Structure

```
pyjsonparser/
├── src/pyjson/
│   ├── abstract/           # Abstract base contracts
│   ├── core/
│   │   ├── lexer/         # Tokenization logic
│   │   ├── parser/        # Parsing logic
│   │   └── shared/        # Shared constants
│   └── impl/              # Concrete implementations
└── tests/                 # Test suite
```

## Development

Run tests:
```bash
poetry run pytest
```

## Author

Ionut-Alexandru Prodan (prodanalexandru1999@gmail.com)

## License

See LICENSE file for details.
