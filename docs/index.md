# PyJSONParser Documentation

Welcome to the documentation for **`pyjsonparser`** (`pyjson`), a clean, modular JSON parser and serializer written in Python 3.12+.

Unlike monolithic parser implementations, `pyjsonparser` decouples lexical analysis (tokenization), recursive descent parsing, and serialization into distinct, contract-driven components. This makes it an excellent choice for learning language parser design, creating custom JSON-like dialects, or extending JSON syntax.

---

## 🌟 Key Highlights

- **Complete JSON Support**: Full support for JSON objects, arrays, strings, integers, floats, booleans (`true`/`false`), and `null`.
- **Lexer-Parser Architecture**: Separates lexical analysis from structural parsing via abstract base contracts.
- **Bi-directional Processing**:
  - `from_string(string)`: Deserializes JSON string into native Python dictionaries, lists, and primitives.
  - `to_string(object)`: Serializes Python dictionaries, lists, and primitives into JSON strings.
- **Extensible Design**: Abstract base classes (`JsonParserContract`, `LexContract`, `ParserContract`) allow swapping or extending components.
- **Clean Python 3.12+ Code**: Type annotations, zero external runtime dependencies, and comprehensive unit tests.

---

## 🚀 Quick Example

```python
from pyjson import JsonParser

parser = JsonParser()

# 1. Parse JSON to Python
raw_json = '{"name": "Alice", "score": 98.5, "active": true, "skills": ["python", "c++"]}'
data = parser.from_string(raw_json)
print(data)
# Output: {'name': 'Alice', 'score': 98.5, 'active': True, 'skills': ['python', 'c++']}

# 2. Serialize Python to JSON
payload = {"status": "ok", "items": [1, 2, 3], "archived": False}
json_str = parser.to_string(payload)
print(json_str)
# Output: {"status": "Alice", "items": [1, 2, 3], "archived": false}
```

---

## 📚 Documentation Index

- [Getting Started](getting-started.md): Installation instructions, requirements, and basic usage.
- [Architecture & Design](architecture.md): Deep dive into the Lexer, Parser, and Serialization pipeline.
- [API Reference](api-reference.md): Detailed classes, contracts, methods, and constants documentation.
- [Usage Examples](examples.md): Practical code recipes, custom extensions, and error handling.
- [Contributing & Development](contributing.md): Setting up local development, running tests, and publishing releases.
