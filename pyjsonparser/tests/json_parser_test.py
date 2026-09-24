"""Unit tests for the pyjson parser, lexer, and serializer."""

from pyjson import JsonParser
from pyjson.core.lexer.impl.lex import Lexer
from pyjson.core.parser.impl.parser import Parser


def test_empty_object():
    """Verify parsing of an empty JSON object `{}`."""
    parser = JsonParser()
    assert parser.from_string('{}') == {}


def test_basic_object():
    """Verify parsing of a simple key-value object with strings."""
    parser = JsonParser()
    assert parser.from_string('{"foo":"bar"}') == {"foo": "bar"}


def test_basic_number():
    """Verify parsing of integer numbers as object values."""
    parser = JsonParser()
    assert parser.from_string('{"foo":1}') == {"foo": 1}


def test_empty_array():
    """Verify parsing of an empty array as an object value."""
    parser = JsonParser()
    assert parser.from_string('{"foo":[]}') == {"foo": []}


def test_basic_array():
    """Verify parsing of mixed-type array elements (integers and strings)."""
    parser = JsonParser()
    assert parser.from_string('{"foo":[1,2,"three"]}') == {
        "foo": [1, 2, "three"]}


def test_nested_object():
    """Verify parsing of nested object hierarchies."""
    parser = JsonParser()
    assert parser.from_string('{"foo":{"bar":2}}') == {"foo": {"bar": 2}}


def test_true():
    """Verify parsing of boolean true literal into Python True."""
    parser = JsonParser()
    assert parser.from_string('{"foo":true}') == {"foo": True}


def test_false():
    """Verify parsing of boolean false literal into Python False."""
    parser = JsonParser()
    assert parser.from_string('{"foo":false}') == {"foo": False}


def test_null():
    """Verify parsing of null literal into Python None."""
    parser = JsonParser()
    assert parser.from_string('{"foo":null}') == {"foo": None}


def test_basic_whitespace():
    """Verify that ignored whitespace (spaces around tokens) does not affect parsing."""
    parser = JsonParser()
    assert parser.from_string('{ "foo" : [1, 2, "three"] }') == {
        "foo": [1, 2, "three"]}


def test_to_string_serialization():
    """Verify serialization from Python dict back into JSON string format."""
    parser = JsonParser()
    sample = {"name": "Alice", "admin": True, "roles": ["dev", "lead"], "age": 30}
    json_str = parser.to_string(sample)
    # Re-parsing should equal original Python structure
    assert parser.from_string(json_str) == sample


def test_core():
    """Verify the decoupled Lexer and Parser components directly."""
    lexer = Lexer()
    parser = Parser()

    # Step 1: Tokenize
    actual = lexer.get_tokens('{"foo": [1, 2, {"bar": 2}]}')
    expected = ['{', 'foo', ':', '[', 1, ',', 2,
                ',', '{', 'bar', ':', 2, '}', ']', '}']
    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(expected, actual))

    # Step 2: Parse tokens
    parse_result = parser.parse(actual, is_root=True)
    assert {"foo": [1, 2, {"bar": 2}]} == parse_result[0]
    assert not len(parse_result[1])
