"""Abstract contract defining lexical analysis for tokenizing JSON strings."""

from abc import ABC, abstractmethod
from typing import List, Tuple, Union
from pyjson.core.shared.constants import JSON_SYNTAX, JSON_WHITESPACE


class LexContract(ABC):
    """Abstract base class defining the contract for JSON tokenization (lexical analysis).

    Implements the tokenization loop in `get_tokens()` by sequentially attempting to match
    literal strings, numbers, booleans, null, whitespace, and syntax delimiters.
    """

    def get_tokens(self, string: str) -> List[str]:
        """Tokenizes an entire JSON string into a list of constituent tokens.

        Scans the input string sequentially and uses greedy matching to identify:
        - Quoted strings (via `lex_string`)
        - Numbers (via `lex_number`)
        - Booleans (via `lex_bool`)
        - Null literals (via `lex_null`)
        - Single-character structural delimiters (e.g. `{`, `}`, `[`, `]`, `:`, `,`)
        - Skipped whitespace (spaces, tabs, newlines)

        Args:
            string: The raw JSON string to tokenize.

        Returns:
            List[str]: Ordered sequence of tokens extracted from the input string.

        Raises:
            Exception: If string is None or contains unrecognized / invalid characters.
        """
        if string is None:
            raise Exception("Unable to parse json.")

        tokens = []
        while len(string):
            # 1. Try matching a double-quoted string
            json_string, string = self.lex_string(string)
            if json_string is not None:
                tokens.append(json_string)
                continue

            # 2. Try matching a numeric literal (int or float)
            json_number, string = self.lex_number(string)
            if json_number is not None:
                tokens.append(json_number)
                continue

            # 3. Try matching boolean literals (true / false)
            json_bool, string = self.lex_bool(string)
            if json_bool is not None:
                tokens.append(json_bool)
                continue

            # 4. Try matching null literal
            json_null, string = self.lex_null(string)
            if json_null is not None:
                tokens.append(None)
                continue

            # 5. Skip whitespace characters
            if string[0] in JSON_WHITESPACE:
                string = string[1:]
            # 6. Capture structural delimiters ({, }, [, ], :, ,)
            elif string[0] in JSON_SYNTAX:
                tokens.append(string[0])
                string = string[1:]
            else:
                raise Exception("Unable to parse json.")

        return tokens

    @abstractmethod
    def lex_string(self, string: str) -> Tuple[str, str]:
        """Extracts a quoted string token from the beginning of string.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[str, str]: (Extracted string content without quotes, remaining unparsed string).
                Returns (None, string) if the current character is not a quote.
        """
        pass

    @abstractmethod
    def lex_number(self, string: str) -> Tuple[Union[int, float], str]:
        """Extracts a numeric literal token from the beginning of string.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[Union[int, float], str]: (Parsed int or float, remaining unparsed string).
                Returns (None, string) if no numeric literal is found.
        """
        pass

    @abstractmethod
    def lex_bool(self, string: str) -> Tuple[bool, str]:
        """Extracts a boolean token (True or False) from the beginning of string.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[bool, str]: (Parsed bool, remaining unparsed string).
                Returns (None, string) if no boolean literal is found.
        """
        pass

    @abstractmethod
    def lex_null(self, string: str) -> Tuple[Union[True, None], str]:
        """Extracts a null token from the beginning of string.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[Union[True, None], str]: (True if 'null' matched, remaining unparsed string).
                Returns (None, string) if no null literal is found.
        """
        pass
