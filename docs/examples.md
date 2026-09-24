# Usage Examples & Recipes

Practical examples and recipes for using and extending `pyjsonparser`.

---

## 1. Parsing Nested Data Structures

`pyjsonparser` supports arbitrarily nested JSON structures, mixing objects and arrays:

```python
from pyjson import JsonParser

parser = JsonParser()

payload = """
{
    "company": "TechCorp",
    "departments": [
        {
            "name": "Engineering",
            "headcount": 42,
            "remote_friendly": true,
            "budget": 1250000.75,
            "teams": ["Core", "Platform", "QA"]
        },
        {
            "name": "Design",
            "headcount": 8,
            "remote_friendly": false,
            "budget": null,
            "teams": ["Brand", "Product"]
        }
    ]
}
"""

data = parser.from_string(payload)

# Accessing nested structures
print(data["company"])
# 'TechCorp'

print(data["departments"][0]["name"])
# 'Engineering'

print(data["departments"][0]["teams"])
# ['Core', 'Platform', 'QA']

print(data["departments"][1]["budget"])
# None
```

---

## 2. Serializing Python Dictionaries and Lists

You can convert native Python data structures into a clean JSON string with `to_string()`:

```python
from pyjson import JsonParser

parser = JsonParser()

dataset = {
    "server": "us-east-1",
    "ports": [80, 443, 8080],
    "ssl_enabled": True,
    "maintenance": None
}

json_output = parser.to_string(dataset)
print(json_output)
# {"server": "us-east-1", "ports": [80, 443, 8080], "ssl_enabled": true, "maintenance": null}
```

---

## 3. Working Directly with the Lexer

You can use `Lexer` independently to tokenize a string without building the final Python object. This is useful for building syntax highlighters or linters:

```python
from pyjson.core.lexer.impl.lex import Lexer

lexer = Lexer()
tokens = lexer.get_tokens('{"id": 101, "valid": true}')
print(tokens)
# ['{', 'id', ':', 101, ',', 'valid', ':', True, '}']
```

---

## 4. Working Directly with the Parser

You can feed custom token lists directly into the `Parser`:

```python
from pyjson.core.parser.impl.parser import Parser

parser = Parser()
tokens = ['{', 'key', ':', 'value', '}']

result, remaining_tokens = parser.parse(tokens, is_root=True)
print(result)            # {'key': 'value'}
print(remaining_tokens)  # []
```

---

## 5. Error Handling

`pyjsonparser` raises exceptions when encountering malformed JSON syntax:

### Non-closing Quotes

```python
from pyjson import JsonParser

parser = JsonParser()

try:
    parser.from_string('{"name": "Alice}')
except Exception as e:
    print(f"Caught error: {e}")
    # Caught error: Unable to parse json (non closing quotes)
```

### Missing End Brace / Bracket

```python
from pyjson import JsonParser

parser = JsonParser()

try:
    parser.from_string('{"name": "Alice"')
except Exception as e:
    print(f"Caught error: {e}")
    # Caught error: Expected end-of-object brace
```

### Non-Object at Root

By default, the JSON parser requires the root entity to be an object (`{...}`):

```python
from pyjson import JsonParser

parser = JsonParser()

try:
    parser.from_string('["item1", "item2"]')
except Exception as e:
    print(f"Caught error: {e}")
    # Caught error: Root must be an object
```
