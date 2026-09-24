"""pyjson: A modular JSON parser and serializer written in Python.

This package provides a decoupled lexer-parser architecture for parsing JSON strings
into native Python data structures and serializing Python objects back into JSON strings.

Primary Export:
    JsonParser: High-level parser and serializer class implementing JsonParserContract.
"""

from pyjson.impl import JsonParser

__all__ = ["JsonParser"]
