from src.pyjson import JsonParser
from src.pyjson.core.lexer.impl.lex import Lexer
from src.pyjson.core.parser.impl.parser import Parser


def test_empty_object():
    parser = JsonParser()
    assert parser.from_string('{}') == {}


def test_basic_object():
    parser = JsonParser()
    assert parser.from_string('{"foo":"bar"}') == {"foo": "bar"}


def test_basic_number():
    parser = JsonParser()
    assert parser.from_string('{"foo":1}') == {"foo": 1}


def test_empty_array():
    parser = JsonParser()
    assert parser.from_string('{"foo":[]}') == {"foo": []}


def test_basic_array():
    parser = JsonParser()
    assert parser.from_string('{"foo":[1,2,"three"]}') == {
        "foo": [1, 2, "three"]}


def test_nested_object():
    parser = JsonParser()
    assert parser.from_string('{"foo":{"bar":2}}') == {"foo": {"bar": 2}}


def test_true():
    parser = JsonParser()
    assert parser.from_string('{"foo":true}') == {"foo": True}


def test_false():
    parser = JsonParser()
    assert parser.from_string('{"foo":false}') == {"foo": False}


def test_null():
    parser = JsonParser()
    assert parser.from_string('{"foo":null}') == {"foo": None}


def test_basic_whitespace():
    parser = JsonParser()
    assert parser.from_string('{ "foo" : [1, 2, "three"] }') == {
        "foo": [1, 2, "three"]}


def test_core():
    lexer = Lexer()
    parser = Parser()
    actual = lexer.get_tokens('{"foo": [1, 2, {"bar": 2}]}')
    expected = ['{', 'foo', ':', '[', 1, ',', 2,
                ',', '{', 'bar', ':', 2, '}', ']', '}']
    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(expected, actual))
    parse_result = parser.parse(actual, is_root=True)
    assert {"foo": [1, 2, {"bar": 2}]} == parse_result[0]
    assert not len(parse_result[1])
