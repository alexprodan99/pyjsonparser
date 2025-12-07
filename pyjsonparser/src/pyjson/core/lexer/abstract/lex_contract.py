from abc import ABC, abstractmethod
from typing import List, Tuple, Union
from src.pyjson.core.shared.constants import *


class LexContract(ABC):
    def get_tokens(self, string: str) -> List[str]:
        if string is None:
            raise Exception("Unable to parse json.")

        tokens = []
        while len(string):
            json_string, string = self.lex_string(string)
            if json_string is not None:
                tokens.append(json_string)
                continue

            json_number, string = self.lex_number(string)
            if json_number is not None:
                tokens.append(json_number)
                continue

            json_bool, string = self.lex_bool(string)
            if json_bool is not None:
                tokens.append(json_bool)
                continue

            json_null, string = self.lex_null(string)
            if json_null is not None:
                tokens.append(None)
                continue

            if string[0] in JSON_WHITESPACE:
                string = string[1:]
            elif string[0] in JSON_SYNTAX:
                tokens.append(string[0])
                string = string[1:]
            else:
                raise Exception("Unable to parse json.")
        return tokens

    @abstractmethod
    def lex_string(self, string: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    def lex_number(self, string: str) -> Tuple[Union[int, float], str]:
        pass

    @abstractmethod
    def lex_bool(self, string: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def lex_null(self, string: str) -> Tuple[Union[True, None], str]:
        pass
