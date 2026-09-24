"""Concrete implementation of ParserContract for recursive descent parsing."""

from typing import List, Tuple
from pyjson.core.parser.abstract.parser_contract import ParserContract
from pyjson.core.shared.constants import (
    JSON_COLON,
    JSON_COMMA,
    JSON_RIGHTBRACKET,
    JSON_RIGHTBRACE,
)


class Parser(ParserContract):
    """Concrete recursive descent parser for JSON token streams.

    Parses tokens into Python dictionaries, lists, and primitives.
    """

    def parse_array(self, tokens: List[str]) -> Tuple[object, List[str]]:
        """Parses elements of a JSON array enclosed in `[...]`.

        Expects zero or more values separated by commas, ending with `]`.

        Args:
            tokens: Token stream positioned immediately after the opening `[`.

        Returns:
            Tuple[object, List[str]]: (List of parsed values, remaining unparsed tokens).

        Raises:
            Exception: If elements are not properly comma-separated or if the
                closing bracket `]` is missing.
        """
        json_array = []

        # Check for immediate empty array: `[]`
        token = tokens[0]
        if token == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]

        # Iterate and recursively parse array items
        while len(tokens):
            # Parse the next element in the array
            json, tokens = self.parse(tokens)
            json_array.append(json)

            # Check next delimiter after the element
            token = tokens[0]
            if token == JSON_RIGHTBRACKET:
                # Array completed
                return json_array, tokens[1:]
            elif token != JSON_COMMA:
                raise Exception('Expected comma after object in array')
            else:
                # Consume comma and proceed to next element
                tokens = tokens[1:]

        raise Exception('Expected end-of-array bracket')

    def parse_object(self, tokens: List[str]) -> Tuple[object, List[str]]:
        """Parses key-value pairs of a JSON object enclosed in `{...}`.

        Expects alternating string keys, colons `:`, and recursively parsed values,
        separated by commas and terminated by a closing brace `}`.

        Args:
            tokens: Token stream positioned immediately after the opening `{`.

        Returns:
            Tuple[object, List[str]]: (Dictionary of key-value pairs, remaining unparsed tokens).

        Raises:
            Exception: If a key is not a string, if the colon is missing, if pairs
                are not comma-separated, or if the closing brace `}` is missing.
        """
        json_object = {}

        # Check for immediate empty object: `{}`
        token = tokens[0]
        if token == JSON_RIGHTBRACE:
            return json_object, tokens[1:]

        # Iterate and parse key-value pairs
        while len(tokens):
            # 1. Extract and validate string key
            json_key = tokens[0]
            if type(json_key) is str:
                tokens = tokens[1:]
            else:
                raise Exception(
                    'Expected string key, got: {}'.format(json_key))

            # 2. Validate colon delimiter after key
            if tokens[0] != JSON_COLON:
                raise Exception(
                    'Expected colon after key in object, got: {}'.format(tokens[0]))

            # 3. Recursively parse the associated value (after colon)
            json_value, tokens = self.parse(tokens[1:])
            json_object[json_key] = json_value

            # 4. Check delimiter after value: must be closing `}` or comma `,`
            token = tokens[0]
            if token == JSON_RIGHTBRACE:
                # Object completed
                return json_object, tokens[1:]
            elif token != JSON_COMMA:
                raise Exception(
                    'Expected comma after pair in object, got: {}'.format(token))

            # Consume comma and proceed to next key-value pair
            tokens = tokens[1:]

        raise Exception('Expected end-of-object brace')
