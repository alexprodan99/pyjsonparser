"""Shared lexical and syntactic constants for JSON grammar and parsing.

Defines delimiter characters, whitespace sets, structural tokens, and literal
lengths conforming to the JSON specification (RFC 8259).
"""

# Structural Delimiters
JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTBRACKET = '['
JSON_RIGHTBRACKET = ']'
JSON_LEFTBRACE = '{'
JSON_RIGHTBRACE = '}'
JSON_QUOTE = '"'

# Whitespace characters ignored during tokenization
JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']

# All valid single-character structural tokens in JSON grammar
JSON_SYNTAX = [
    JSON_COMMA,
    JSON_COLON,
    JSON_LEFTBRACKET,
    JSON_RIGHTBRACKET,
    JSON_LEFTBRACE,
    JSON_RIGHTBRACE,
]

# Character lengths for literal keywords used during fast prefix matching
FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')
