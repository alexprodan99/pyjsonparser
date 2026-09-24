"""Comprehensive unit tests for the pyjson parser, lexer, and serializer.

Covers:
- JSON Objects (empty, flat, multiple keys, deeply nested)
- JSON Arrays (empty, flat, nested arrays, arrays of objects)
- Data Types (integers, floats, negative numbers, zero, scientific notation, strings, booleans, null)
- Whitespace handling (spaces, tabs, newlines, carriage returns)
- Serialization (to_string for dicts, lists, primitives, empty structures, round-trip)
- Error handling (unclosed quotes, missing braces/brackets, syntax errors, non-object roots)
- Direct Lexer & Parser component tests
"""

import pytest
from pyjson import JsonParser
from pyjson.core.lexer.impl.lex import Lexer
from pyjson.core.parser.impl.parser import Parser


# =====================================================================
# Object Parsing Tests
# =====================================================================

def test_empty_object():
    """Verify parsing of an empty JSON object `{}`."""
    parser = JsonParser()
    assert parser.from_string('{}') == {}


def test_basic_object():
    """Verify parsing of a simple key-value object with strings."""
    parser = JsonParser()
    assert parser.from_string('{"foo":"bar"}') == {"foo": "bar"}


def test_multiple_keys_object():
    """Verify parsing of an object with multiple diverse keys."""
    parser = JsonParser()
    raw = '{"name": "Alice", "age": 30, "city": "Paris", "active": true}'
    expected = {"name": "Alice", "age": 30, "city": "Paris", "active": True}
    assert parser.from_string(raw) == expected


def test_nested_object():
    """Verify parsing of nested object hierarchies."""
    parser = JsonParser()
    assert parser.from_string('{"foo":{"bar":2}}') == {"foo": {"bar": 2}}


def test_deeply_nested_hierarchy():
    """Verify parsing of multiple levels of nested objects and arrays."""
    parser = JsonParser()
    raw = '{"lvl1": {"lvl2": {"lvl3": {"value": 42, "items": [1, [2, 3]]}}}}'
    expected = {
        "lvl1": {
            "lvl2": {
                "lvl3": {
                    "value": 42,
                    "items": [1, [2, 3]]
                }
            }
        }
    }
    assert parser.from_string(raw) == expected


# =====================================================================
# Array Parsing Tests
# =====================================================================

def test_empty_array():
    """Verify parsing of an empty array as an object value."""
    parser = JsonParser()
    assert parser.from_string('{"foo":[]}') == {"foo": []}


def test_basic_array():
    """Verify parsing of mixed-type array elements (integers and strings)."""
    parser = JsonParser()
    assert parser.from_string('{"foo":[1,2,"three"]}') == {"foo": [1, 2, "three"]}


def test_nested_arrays():
    """Verify parsing of multi-dimensional nested arrays (matrices)."""
    parser = JsonParser()
    raw = '{"matrix": [[1, 2], [3, 4], [5, 6]]}'
    expected = {"matrix": [[1, 2], [3, 4], [5, 6]]}
    assert parser.from_string(raw) == expected


def test_array_of_objects():
    """Verify parsing of an array containing multiple JSON objects."""
    parser = JsonParser()
    raw = '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}'
    expected = {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }
    assert parser.from_string(raw) == expected


def test_array_with_booleans_and_null():
    """Verify parsing of arrays containing boolean literals and null."""
    parser = JsonParser()
    assert parser.from_string('{"items": [true, false, null]}') == {
        "items": [True, False, None]
    }


# =====================================================================
# Number Parsing Tests (Integers, Floats, Scientific Notation)
# =====================================================================

def test_basic_number():
    """Verify parsing of positive integer numbers."""
    parser = JsonParser()
    assert parser.from_string('{"foo":1}') == {"foo": 1}


def test_zero():
    """Verify parsing of zero."""
    parser = JsonParser()
    assert parser.from_string('{"zero":0}') == {"zero": 0}


def test_negative_integers():
    """Verify parsing of negative integers."""
    parser = JsonParser()
    assert parser.from_string('{"temp": -42, "offset": -1}') == {
        "temp": -42,
        "offset": -1
    }


def test_floats():
    """Verify parsing of positive floating point numbers."""
    parser = JsonParser()
    assert parser.from_string('{"pi": 3.14159, "ratio": 0.5}') == {
        "pi": 3.14159,
        "ratio": 0.5
    }


def test_negative_floats():
    """Verify parsing of negative floating point numbers."""
    parser = JsonParser()
    assert parser.from_string('{"val": -12.34}') == {"val": -12.34}


def test_scientific_notation():
    """Verify parsing of numbers with exponent / scientific notation."""
    parser = JsonParser()
    result = parser.from_string('{"small": 1e-4, "large": 2.5e3, "cap": 1E5}')
    assert result["small"] == 1e-4
    assert result["large"] == 2500.0
    assert result["cap"] == 100000.0


# =====================================================================
# String Parsing Tests
# =====================================================================

def test_empty_string():
    """Verify parsing of an empty string `""`."""
    parser = JsonParser()
    assert parser.from_string('{"empty": ""}') == {"empty": ""}


def test_string_with_spaces_and_special_chars():
    """Verify parsing of strings containing spaces, slashes, and symbols."""
    parser = JsonParser()
    raw = '{"url": "https://example.com/api?q=hello+world&lang=en#top"}'
    assert parser.from_string(raw) == {
        "url": "https://example.com/api?q=hello+world&lang=en#top"
    }


def test_numeric_and_boolean_string_literals():
    """Verify that numbers or booleans inside quotes remain strings and are not coerced."""
    parser = JsonParser()
    raw = '{"str_num": "123", "str_bool": "true", "str_null": "null"}'
    assert parser.from_string(raw) == {
        "str_num": "123",
        "str_bool": "true",
        "str_null": "null"
    }


# =====================================================================
# Boolean and Null Literal Tests
# =====================================================================

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


# =====================================================================
# Whitespace Handling Tests
# =====================================================================

def test_basic_whitespace():
    """Verify that ignored whitespace (spaces around tokens) does not affect parsing."""
    parser = JsonParser()
    assert parser.from_string('{ "foo" : [1, 2, "three"] }') == {
        "foo": [1, 2, "three"]}


def test_multiline_whitespace_with_tabs_and_newlines():
    """Verify parsing of formatted JSON with newlines, carriage returns, and tabs."""
    parser = JsonParser()
    raw = """
    {\r
        \t"id": 100,\n
        \t"profile": {\r
            \t\t"name": "Jane",\n
            \t\t"active": true\r
        \t}\n
    }
    """
    assert parser.from_string(raw) == {
        "id": 100,
        "profile": {
            "name": "Jane",
            "active": True
        }
    }


# =====================================================================
# Serialization (to_string) Tests
# =====================================================================

def test_serialize_empty_object():
    """Verify serialization of an empty Python dictionary `{}` into `{}`."""
    parser = JsonParser()
    assert parser.to_string({}) == '{}'


def test_serialize_empty_array():
    """Verify serialization of an empty Python list `[]` into `[]`."""
    parser = JsonParser()
    assert parser.to_string([]) == '[]'


def test_serialize_primitives():
    """Verify serialization of individual scalar types."""
    parser = JsonParser()
    assert parser.to_string("hello") == '"hello"'
    assert parser.to_string(42) == '42'
    assert parser.to_string(3.14) == '3.14'
    assert parser.to_string(True) == 'true'
    assert parser.to_string(False) == 'false'
    assert parser.to_string(None) == 'null'


def test_serialize_nested_structure():
    """Verify serialization of complex structures with nested dicts and lists."""
    parser = JsonParser()
    data = {
        "title": "Report",
        "values": [1, 2, 3],
        "meta": {"verified": True, "notes": None}
    }
    serialized = parser.to_string(data)
    assert '"title": "Report"' in serialized
    assert '"values": [1, 2, 3]' in serialized
    assert '"verified": true' in serialized
    assert '"notes": null' in serialized


def test_to_string_serialization_roundtrip():
    """Verify bidirectional roundtrip: deserializing serialized output reproduces the original data."""
    parser = JsonParser()
    sample = {
        "name": "Alice",
        "admin": True,
        "empty_obj": {},
        "empty_arr": [],
        "roles": ["dev", "lead"],
        "age": 30,
        "score": 99.5,
        "notes": None
    }
    json_str = parser.to_string(sample)
    assert parser.from_string(json_str) == sample


# =====================================================================
# Core Lexer and Parser Direct Unit Tests
# =====================================================================

def test_core_integration():
    """Verify the decoupled Lexer and Parser components integration directly."""
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


def test_lexer_lex_number_direct():
    """Verify Lexer.lex_number directly with integers, floats, and leftovers."""
    lexer = Lexer()
    num, rest = lexer.lex_number("123, remaining")
    assert num == 123
    assert rest == ", remaining"

    float_num, rest = lexer.lex_number("45.67] rest")
    assert float_num == 45.67
    assert rest == "] rest"

    neg_num, rest = lexer.lex_number("-999}")
    assert neg_num == -999
    assert rest == "}"

    # Invalid sequence starting with non-digit
    val, rest = lexer.lex_number("abc")
    assert val is None
    assert rest == "abc"


def test_lexer_lex_string_direct():
    """Verify Lexer.lex_string directly."""
    lexer = Lexer()
    s, rest = lexer.lex_string('"hello" : 123')
    assert s == "hello"
    assert rest == " : 123"

    # Non-quoted string returns None
    s, rest = lexer.lex_string('123"hello"')
    assert s is None
    assert rest == '123"hello"'


def test_lexer_lex_bool_and_null_direct():
    """Verify Lexer.lex_bool and Lexer.lex_null directly."""
    lexer = Lexer()
    b_true, rest = lexer.lex_bool("true, next")
    assert b_true is True
    assert rest == ", next"

    b_false, rest = lexer.lex_bool("false, next")
    assert b_false is False
    assert rest == ", next"

    null_val, rest = lexer.lex_null("null, next")
    assert null_val is True
    assert rest == ", next"


def test_parser_array_direct():
    """Verify Parser.parse_array directly."""
    parser = Parser()
    tokens = [1, ',', 2, ',', 3, ']']
    arr, remaining = parser.parse_array(tokens)
    assert arr == [1, 2, 3]
    assert remaining == []


def test_parser_object_direct():
    """Verify Parser.parse_object directly."""
    parser = Parser()
    tokens = ['key', ':', 'value', '}']
    obj, remaining = parser.parse_object(tokens)
    assert obj == {'key': 'value'}
    assert remaining == []


# =====================================================================
# Error and Syntax Handling Tests
# =====================================================================

def test_error_unclosed_quotes():
    """Verify exception on unclosed quotation marks."""
    parser = JsonParser()
    with pytest.raises(Exception, match="non closing quotes"):
        parser.from_string('{"name": "Alice}')


def test_error_missing_closing_brace():
    """Verify exception on missing closing object brace."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Expected end-of-object brace"):
        parser.from_string('{"name": "Alice"')


def test_error_missing_closing_bracket():
    """Verify exception on missing closing array bracket."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Expected end-of-array bracket"):
        parser.from_string('{"arr": [1, 2')


def test_error_missing_comma_in_array():
    """Verify exception when array elements are not separated by comma."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Expected comma after object in array"):
        parser.from_string('{"arr": [1 2]}')


def test_error_missing_colon_in_object():
    """Verify exception when colon is missing after object key."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Expected colon after key in object"):
        parser.from_string('{"key" "value"}')


def test_error_missing_comma_in_object():
    """Verify exception when key-value pairs are not comma-separated."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Expected comma after pair in object"):
        parser.from_string('{"a": 1 "b": 2}')


def test_error_non_string_key():
    """Verify exception when object key is not a string."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Expected string key"):
        parser.from_string('{123: "val"}')


def test_error_root_not_object():
    """Verify exception when root is an array or primitive (enforcing root object contract)."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Root must be an object"):
        parser.from_string('["item1", "item2"]')

    with pytest.raises(Exception, match="Root must be an object"):
        parser.from_string('"just a string"')


def test_error_none_input():
    """Verify exception when input string is None."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Unable to parse json"):
        parser.from_string(None)


def test_error_empty_string_input():
    """Verify exception when input string is empty."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Unable to parse"):
        parser.from_string("")


def test_error_unexpected_token():
    """Verify exception when unexpected / invalid characters are encountered."""
    parser = JsonParser()
    with pytest.raises(Exception, match="Unable to parse json"):
        parser.from_string('{"key": @@@}')
