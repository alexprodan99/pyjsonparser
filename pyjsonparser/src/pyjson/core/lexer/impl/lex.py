"""Concrete implementation of LexContract for tokenizing JSON strings."""

from typing import Tuple, Union
from pyjson.core.lexer.abstract.lex_contract import LexContract
from pyjson.core.shared.constants import (
    FALSE_LEN,
    JSON_QUOTE,
    NULL_LEN,
    TRUE_LEN,
)


class Lexer(LexContract):
    """Concrete lexical analyzer (tokenizer) for JSON text.

    Scans strings and splits them into distinct tokens according to JSON rules.
    """

    def lex_string(self, string: str) -> Tuple[str, str]:
        """Extracts a double-quoted JSON string from the input.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[str, str]: (Extracted string content, remaining unparsed text).
                Returns (None, string) if string does not start with a quote.

        Raises:
            Exception: If an opening quote is found without a matching closing quote.
        """
        json_string = ""
        # Check if the first character is an opening double quote
        if string[0] is not JSON_QUOTE:
            return None, string
        else:
            string = string[1:]

        # Consume characters until the closing quote is encountered
        for char in string:
            if char is not JSON_QUOTE:
                json_string += char
            else:
                # Return the string content and the remaining unconsumed slice
                return json_string, string[len(json_string) + 1:]

        # If loop finishes without finding closing quote, raise syntax error
        raise Exception("Unable to parse json (non closing quotes)")

    def lex_number(self, string: str) -> Tuple[Union[int, float], str]:
        """Extracts an integer or floating-point number from the input.

        Collects contiguous digits, negative sign, decimal points, and scientific
        notation characters ('e').

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[Union[int, float], str]: (Parsed number as int or float, remaining unparsed text).
                Returns (None, string) if no digits or leading minus are found.
        """
        json_number = ''
        number_characters = {str(i) for i in range(10)} | {'e', 'E', '.', '-', '+'}

        # Greedily accumulate valid numeric characters
        for char in string:
            if char in number_characters:
                json_number += char
            else:
                break

        rest = string[len(json_number):]
        if not len(json_number):
            return None, string

        # Safely convert to float or int; return None if malformed (e.g. lone '-')
        try:
            if '.' in json_number or 'e' in json_number.lower():
                return float(json_number), rest
            return int(json_number), rest
        except ValueError:
            return None, string

    def lex_bool(self, string: str) -> Tuple[bool, str]:
        """Extracts a boolean literal ('true' or 'false') from the input.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[bool, str]: (Parsed boolean value, remaining unparsed text).
                Returns (None, string) if no boolean literal matches.
        """
        string_len = len(string)

        # Match exact 'true' literal prefix
        if string_len >= TRUE_LEN and string[:TRUE_LEN] == 'true':
            return True, string[TRUE_LEN:]
        # Match exact 'false' literal prefix
        elif string_len >= FALSE_LEN and string[:FALSE_LEN] == 'false':
            return False, string[FALSE_LEN:]

        return None, string

    def lex_null(self, string: str) -> Tuple[Union[True, None], str]:
        """Extracts a null literal ('null') from the input.

        Args:
            string: Remaining unparsed character stream.

        Returns:
            Tuple[Union[True, None], str]: (True if 'null' matched, remaining unparsed text).
                Returns (None, string) if no null literal matches.
        """
        string_len = len(string)

        # Match exact 'null' literal prefix
        if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
            return True, string[NULL_LEN:]

        return None, string
