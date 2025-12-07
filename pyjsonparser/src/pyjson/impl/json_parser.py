from src.pyjson.abstract import JsonParserContract
from src.pyjson.core import Lexer, Parser


class JsonParser(JsonParserContract):
    def __init__(self):
        self._lexer = Lexer()
        self._parser = Parser()

    def from_string(self, string: str) -> object:
        tokens = self._lexer.get_tokens(string)
        return self._parser.parse(tokens=tokens, is_root=True)[0]

    def to_string(self, json: object) -> str:
        json_type = type(json)

        if json_type is dict:
            string = '{'
            dict_len = len(json)

            for i, (key, val) in enumerate(json.items()):
                string += '"{}": {}'.format(key, self.to_string(val))

                if i < dict_len - 1:
                    string += ', '
                else:
                    string += '}'

            return string
        elif json_type is list:
            string = '['
            list_len = len(json)

            for i, val in enumerate(json):
                string += self.to_string(val)

                if i < list_len - 1:
                    string += ', '
                else:
                    string += ']'

            return string
        elif json_type is str:
            return '"{}"'.format(json)
        elif json_type is bool:
            return 'true' if json else 'false'
        elif json_type is None:
            return 'null'

        return str(json)
