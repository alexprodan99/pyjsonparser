"""Abstract contract defining recursive descent parsing of JSON token streams."""

from abc import ABC, abstractmethod
from typing import List, Tuple
from pyjson.core.shared.constants import JSON_LEFTBRACE, JSON_LEFTBRACKET


class ParserContract(ABC):
    """Abstract base class defining the contract for JSON syntactic parsing.

    Implements the core dispatch logic in `parse()`, determining whether the current
    token represents a JSON object (`{`), a JSON array (`[`), or a scalar primitive value.
    """

    def parse(self, tokens: List[str], is_root: bool = False) -> Tuple[object, List[str]]:
        """Parses the next JSON entity from a token stream.

        Args:
            tokens: Ordered list of unparsed tokens from the lexer.
            is_root: If True, enforces that the initial token must be an opening brace `{`
                representing a JSON root object. Defaults to False.

        Returns:
            Tuple[object, List[str]]: (Parsed Python object, remaining unparsed tokens).

        Raises:
            Exception: If tokens list is empty or if is_root is True and root is not an object.
        """
        # Ensure there are tokens remaining to inspect
        if not tokens or not len(tokens):
            raise Exception("Unable to parse (no tokens)")

        token = tokens[0]

        # Enforce that the root entity must be a JSON object
        if is_root and token != JSON_LEFTBRACE:
            raise Exception('Root must be an object')

        # Array branch: recursively parse array elements starting after '['
        if token is JSON_LEFTBRACKET:
            return self.parse_array(tokens[1:])
        # Object branch: recursively parse key-value pairs starting after '{'
        elif token is JSON_LEFTBRACE:
            return self.parse_object(tokens[1:])

        # Primitive branch: return scalar value and the rest of tokens
        return token, tokens[1:]

    @abstractmethod
    def parse_array(self, tokens: List[str]) -> Tuple[object, List[str]]:
        """Parses a JSON array entity from the token stream.

        Args:
            tokens: Token stream positioned immediately after the opening bracket `[`.

        Returns:
            Tuple[object, List[str]]: (List of parsed array items, remaining tokens after `]`).
        """
        pass

    @abstractmethod
    def parse_object(self, tokens: List[str]) -> Tuple[object, List[str]]:
        """Parses a JSON object entity from the token stream.

        Args:
            tokens: Token stream positioned immediately after the opening brace `{`.

        Returns:
            Tuple[object, List[str]]: (Dictionary of parsed key-value pairs, remaining tokens after `}`).
        """
        pass
