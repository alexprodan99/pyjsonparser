# pyjsonparser

[![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://alexprodan99.github.io/pyjsonparser/)

A custom JSON parser and serializer written in Python, featuring a modular lexer-parser architecture.

## Installation

```bash
pip install pyjsonparser
```

## Requirements

- Python >= 3.12

## Quick Start

```python
from pyjson import JsonParser

parser = JsonParser()

# Parse a JSON string
json_object = parser.from_string('{"name": "John", "age": 30, "active": true}')
# Result: {'name': 'John', 'age': 30, 'active': True}

# Serialize a Python object back to JSON
json_string = parser.to_string({"name": "John", "age": 30, "active": True})
# Result: '{"name": "John", "age": 30, "active": true}'
```

## Documentation

The complete documentation is hosted online at **[alexprodan99.github.io/pyjsonparser](https://alexprodan99.github.io/pyjsonparser/)**.

You can also browse the documentation source files directly in the [`docs/`](https://github.com/alexprodan99/pyjsonparser/tree/main/docs) directory:

- [Getting Started](https://github.com/alexprodan99/pyjsonparser/blob/main/docs/getting-started.md)
- [Architecture & Design](https://github.com/alexprodan99/pyjsonparser/blob/main/docs/architecture.md)
- [API Reference](https://github.com/alexprodan99/pyjsonparser/blob/main/docs/api-reference.md)
- [Usage Examples](https://github.com/alexprodan99/pyjsonparser/blob/main/docs/examples.md)
- [Contributing & Development](https://github.com/alexprodan99/pyjsonparser/blob/main/docs/contributing.md)

## License

Apache License 2.0. See LICENSE for details.