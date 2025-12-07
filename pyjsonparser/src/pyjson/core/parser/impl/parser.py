from typing import List, Tuple
from src.pyjson.core.shared.constants import *
from src.pyjson.core.parser.abstract.parser_contract import ParserContract


class Parser(ParserContract):
    def parse_array(self, tokens: List[str]) -> Tuple[object, List[str]]:
        json_array = []

        token = tokens[0]
        if token == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]

        while len(tokens):
            json, tokens = self.parse(tokens)
            json_array.append(json)

            token = tokens[0]
            if token == JSON_RIGHTBRACKET:
                return json_array, tokens[1:]
            elif token != JSON_COMMA:
                raise Exception('Expected comma after object in array')
            else:
                tokens = tokens[1:]

        raise Exception('Expected end-of-array bracket')

    def parse_object(self, tokens: List[str]) -> Tuple[object, List[str]]:
        json_object = {}

        token = tokens[0]
        if token == JSON_RIGHTBRACE:
            return json_object, tokens[1:]

        while len(tokens):
            json_key = tokens[0]
            if type(json_key) is str:
                tokens = tokens[1:]
            else:
                raise Exception(
                    'Expected string key, got: {}'.format(json_key))

            if tokens[0] != JSON_COLON:
                raise Exception(
                    'Expected colon after key in object, got: {}'.format(token))

            json_value, tokens = self.parse(tokens[1:])

            json_object[json_key] = json_value

            token = tokens[0]
            if token == JSON_RIGHTBRACE:
                return json_object, tokens[1:]
            elif token != JSON_COMMA:
                raise Exception(
                    'Expected comma after pair in object, got: {}'.format(token))

            tokens = tokens[1:]

        raise Exception('Expected end-of-object brace')
