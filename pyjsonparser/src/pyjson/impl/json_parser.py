"""Concrete implementation of JsonParserContract using the Lexer and Parser."""

from pyjson.abstract import JsonParserContract
from pyjson.core import Lexer, Parser


class JsonParser(JsonParserContract):
    """Primary JSON parser and serializer implementation.

    This class orchestrates lexical analysis (via Lexer) and syntactic parsing
    (via Parser) to convert JSON strings into Python objects, and provides
    recursive serialization of Python objects back into JSON strings.

    Attributes:
        _lexer (Lexer): The tokenization engine.
        _parser (Parser): The syntactic recursive descent parser.
    """

    def __init__(self):
        """Initializes the JsonParser with default Lexer and Parser instances."""
        self._lexer = Lexer()
        self._parser = Parser()

    def from_string(self, string: str) -> object:
        """Parses a JSON string into a corresponding Python data structure.

        Args:
            string: A valid JSON string to deserialize.

        Returns:
            The parsed Python object (e.g. dict, list, primitive).

        Raises:
            Exception: If tokenization fails or if parsing encounters syntax errors.
        """
        # Step 1: Lexical analysis - convert raw string into a list of tokens
        tokens = self._lexer.get_tokens(string)

        # Step 2: Syntactic analysis - parse tokens into Python objects
        # is_root=True enforces that the root element must be a valid JSON object
        return self._parser.parse(tokens=tokens, is_root=True)[0]

    def to_string(self, json: object) -> str:
        """Serializes a Python object into its JSON string representation.

        Supports nested dictionaries, lists, strings, booleans, None (null),
        and numeric values (int, float).

        Args:
            json: The Python object to serialize.

        Returns:
            str: A valid JSON string representation of the input object.
        """
        json_type = type(json)

        # Handle dictionaries -> JSON Objects {"key": value}
        if json_type is dict:
            string = '{'
            dict_len = len(json)

            for i, (key, val) in enumerate(json.items()):
                # Recursively format nested values
                string += '"{}": {}'.format(key, self.to_string(val))

                if i < dict_len - 1:
                    string += ', '
                else:
                    string += '}'

            return string

        # Handle lists -> JSON Arrays [item1, item2]
        elif json_type is list:
            string = '['
            list_len = len(json)

            for i, val in enumerate(json):
                # Recursively format array items
                string += self.to_string(val)

                if i < list_len - 1:
                    string += ', '
                else:
                    string += ']'

            return string

        # Handle strings -> quoted JSON strings
        elif json_type is str:
            return '"{}"'.format(json)

        # Handle booleans -> lowercase true / false
        elif json_type is bool:
            return 'true' if json else 'false'

        # Handle None -> null
        elif json_type is None:
            return 'null'

        # Fallback for numbers (int, float) and other types
        return str(json)
