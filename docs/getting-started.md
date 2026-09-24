# Getting Started

This guide walks you through installing `pyjsonparser` and getting started with parsing and serializing JSON data.

---

## Requirements

- **Python**: `>= 3.12`
- **Runtime Dependencies**: None (Standard Library only)

---

## Installation

### Method 1: Using `pip` (Recommended)

Install the latest release from PyPI:

```bash
pip install pyjsonparser
```

### Method 2: Using Poetry

If you are using Poetry in your project:

```bash
poetry add pyjsonparser
```

### Method 3: From Source

Clone the GitHub repository to work with the latest development code:

```bash
git clone https://github.com/alexprodan99/pyjsonparser.git
cd pyjsonparser/pyjsonparser
poetry install
```

---

## Verification

Verify your installation by running a quick inline Python test:

```bash
python -c "import pyjson; p = pyjson.JsonParser(); print(p.from_string('{\"status\": \"ready\"}'))"
```

Output:
```python
{'status': 'ready'}
```

---

## Basic Usage

### Importing the Parser

The primary entry point of the library is `JsonParser`, exposed directly from the `pyjson` package:

```python
from pyjson import JsonParser

parser = JsonParser()
```

### Parsing JSON Strings (`from_string`)

Pass any valid JSON object string to `from_string()`:

```python
from pyjson import JsonParser

parser = JsonParser()

# Parsing primitive types within an object
data = parser.from_string('''
{
    "title": "Parser Guide",
    "version": 1,
    "rating": 4.95,
    "published": true,
    "metadata": null,
    "tags": ["parser", "python", "json"]
}
''')

print(type(data))          # <class 'dict'>
print(data["title"])       # "Parser Guide"
print(data["version"])     # 1 (int)
print(data["rating"])      # 4.95 (float)
print(data["published"])   # True (bool)
print(data["metadata"])    # None
print(data["tags"])        # ['parser', 'python', 'json']
```

### Serializing to JSON Strings (`to_string`)

Convert Python data structures into a JSON-compliant string:

```python
from pyjson import JsonParser

parser = JsonParser()

user_dict = {
    "username": "johndoe",
    "age": 28,
    "active": True,
    "roles": ["admin", "developer"],
    "preferences": None
}

json_output = parser.to_string(user_dict)
print(json_output)
# {"username": "johndoe", "age": 28, "active": true, "roles": ["admin", "developer"], "preferences": null}
```

---

## Next Steps

- Explore the [Architecture & Design](architecture.md) to understand the lexer-parser pipeline.
- Check the [API Reference](api-reference.md) for full method signatures and contracts.
- Read [Usage Examples](examples.md) for nested structures and advanced patterns.
