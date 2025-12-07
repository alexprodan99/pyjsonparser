from typing import Tuple, Union
from src.pyjson.core.lexer.abstract.lex_contract import LexContract
from src.pyjson.core.shared.constants import *


class Lexer(LexContract):
    def lex_string(self, string: str) -> Tuple[str, str]:
        json_string = ""
        if string[0] is not JSON_QUOTE:
            return None, string
        else:
            string = string[1:]

        for char in string:
            if char is not JSON_QUOTE:
                json_string += char
            else:
                return json_string, string[len(json_string)+1:]
        raise Exception("Unable to parse json (non closing quotes)")

    def lex_number(self, string: str) -> Tuple[Union[int, float], str]:
        json_number = ''
        number_characters = {str(i) for i in range(10)} | {'e', '.', '-'}

        for char in string:
            if char in number_characters:
                json_number += char
            else:
                break

        rest = string[len(json_number):]
        if not len(json_number):
            return None, string
        if '.' in json_number:
            return float(json_number), rest
        return int(json_number), rest

    def lex_bool(self, string: str) -> Tuple[bool, str]:
        string_len = len(string)

        if string_len >= TRUE_LEN and \
                string[:TRUE_LEN] == 'true':
            return True, string[TRUE_LEN:]
        elif string_len >= FALSE_LEN and \
                string[:FALSE_LEN] == 'false':
            return False, string[FALSE_LEN:]

        return None, string

    def lex_null(self, string: str) -> Tuple[Union[True, None], str]:
        string_len = len(string)

        if string_len >= NULL_LEN and \
                string[:NULL_LEN] == 'null':
            return True, string[NULL_LEN:]

        return None, string
