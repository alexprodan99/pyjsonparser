# API Reference

Comprehensive reference documentation for all public contracts, classes, functions, and constants in `pyjsonparser`.

---

## High-Level Interface

### `pyjson.JsonParser`

The main concrete parser class implementing `JsonParserContract`.

```python
from pyjson import JsonParser

parser = JsonParser()
```

#### Methods

##### `from_string(string: str) -> object`
Parses a JSON string and returns the corresponding Python object (typically a `dict`).

- **Parameters**:
  - `string` (*str*): A valid JSON string to parse.
- **Returns**:
  - `object`: The resulting Python data structure (dict, list, string, number, bool, None).
- **Raises**:
  - `Exception`: If the string is malformed, has non-closing quotes, missing brackets/braces, or if the root is not an object.

##### `to_string(json: object) -> str`
Serializes a Python object into a JSON string.

- **Parameters**:
  - `json` (*object*): The Python data structure to serialize (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`).
- **Returns**:
  - `str`: Formatted JSON string representation.

---

## Abstract Contracts

### `pyjson.abstract.JsonParserContract`

Abstract Base Class (`ABC`) defining the contract for high-level JSON parsers.

```python
from abc import ABC, abstractmethod

class JsonParserContract(ABC):
    @abstractmethod
    def from_string(self, string: str) -> object:
        pass

    @abstractmethod
    def to_string(self, json: object) -> str:
        pass
```

---

## Lexer Layer (`pyjson.core.lexer`)

### `pyjson.core.lexer.abstract.LexContract`

Abstract Base Class defining the tokenization interface.

#### Methods

##### `get_tokens(string: str) -> List[str]`
Iterates through `string` and extracts all JSON tokens, ignoring whitespace.

- **Parameters**: `string` (*str*): The input JSON text.
- **Returns**: `List[str]`: Ordered list of extracted tokens.
- **Raises**: `Exception`: If `string` is `None` or contains unrecognized characters.

##### `lex_string(string: str) -> Tuple[str, str]` *(abstract)*
Extracts a double-quoted JSON string token from the start of `string`.

##### `lex_number(string: str) -> Tuple[Union[int, float], str]` *(abstract)*
Extracts an integer or float token from the start of `string`.

##### `lex_bool(string: str) -> Tuple[bool, str]` *(abstract)*
Extracts a boolean (`True` or `False`) from `"true"` or `"false"`.

##### `lex_null(string: str) -> Tuple[Union[True, None], str]` *(abstract)*
Extracts `None` from `"null"`.

---

### `pyjson.core.lexer.impl.Lexer`

The concrete tokenization engine implementing `LexContract`.

```python
from pyjson.core.lexer.impl.lex import Lexer

lexer = Lexer()
tokens = lexer.get_tokens('{"name": "Alice", "age": 30}')
# tokens: ['{', 'name', ':', 'Alice', ',', 'age', ':', 30, '}']
```

---

## Parser Layer (`pyjson.core.parser`)

### `pyjson.core.parser.abstract.ParserContract`

Abstract Base Class defining recursive descent parsing for a token stream.

#### Methods

##### `parse(tokens: List[str], is_root: bool = False) -> Tuple[object, List[str]]`
Parses the next JSON entity from `tokens`.

- **Parameters**:
  - `tokens` (*List[str]*): The remaining list of tokens.
  - `is_root` (*bool*, optional): If `True`, enforces that the root token must be `{`. Default is `False`.
- **Returns**:
  - `Tuple[object, List[str]]`: A tuple containing the parsed Python object and the remaining unparsed tokens.
- **Raises**:
  - `Exception`: If `tokens` is empty or if root is not an object when `is_root=True`.

##### `parse_object(tokens: List[str]) -> Tuple[object, List[str]]` *(abstract)*
Parses a JSON object (`{ ... }`) from the token stream.

##### `parse_array(tokens: List[str]) -> Tuple[object, List[str]]` *(abstract)*
Parses a JSON array (`[ ... ]`) from the token stream.

---

### `pyjson.core.parser.impl.Parser`

The concrete recursive descent parser implementing `ParserContract`.

```python
from pyjson.core.parser.impl.parser import Parser

parser = Parser()
result, remaining = parser.parse(['{', 'foo', ':', 'bar', '}'], is_root=True)
# result: {'foo': 'bar'}
# remaining: []
```

---

## Constants (`pyjson.core.shared.constants`)

The constants module defines the JSON grammar delimiter characters:

| Constant | Value | Description |
| :--- | :--- | :--- |
| `JSON_COMMA` | `','` | Comma separator |
| `JSON_COLON` | `':'` | Key-value separator |
| `JSON_LEFTBRACKET` | `'['` | Array opening bracket |
| `JSON_RIGHTBRACKET` | `']'` | Array closing bracket |
| `JSON_LEFTBRACE` | `'{'` | Object opening brace |
| `JSON_RIGHTBRACE` | `'}'` | Object closing brace |
| `JSON_QUOTE` | `'"'` | String quotation mark |
| `JSON_WHITESPACE` | `[' ', '\t', '\b', '\n', '\r']` | Skipped whitespace characters |
| `JSON_SYNTAX` | List of all structural delimiters | `[',', ':', '[', ']', '{', '}']` |
| `FALSE_LEN` | `5` | Length of `"false"` |
| `TRUE_LEN` | `4` | Length of `"true"` |
| `NULL_LEN` | `4` | Length of `"null"` |
