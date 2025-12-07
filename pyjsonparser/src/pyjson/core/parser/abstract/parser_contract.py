from abc import ABC, abstractmethod
from typing import List, Tuple
from src.pyjson.core.shared.constants import *


class ParserContract(ABC):
    def parse(self, tokens: List[str], is_root=False) -> Tuple[object, List[str]]:
        if not tokens or not len(tokens):
            raise Exception("Unable to parse (no tokens)")

        token = tokens[0]
        if is_root and token != JSON_LEFTBRACE:
            raise Exception('Root must be an object')

        if token is JSON_LEFTBRACKET:
            return self.parse_array(tokens[1:])
        elif token is JSON_LEFTBRACE:
            return self.parse_object(tokens[1:])
        return token, tokens[1:]

    @abstractmethod
    def parse_array(self, tokens: List[str]) -> Tuple[object, List[str]]:
        pass

    @abstractmethod
    def parse_object(self, tokens: List[str]) -> Tuple[object, List[str]]:
        pass
