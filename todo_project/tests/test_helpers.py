
"""
Test suite for the make_upper helper function.

Tests cover:
- Basic functionality of stripping whitespace and converting to uppercase
- Handling of empty strings and whitespace-only strings
- Preservation of internal whitespace while stripping leading/trailing whitespace
- Verification of type annotations (str input and str return type)
"""
# import pytest
from todo.helpers import make_upper

def test_make_upper_strips_and_upcases():
    assert make_upper("   hello there world   ") == "HELLO THERE WORLD"

def test_make_upper_empty_and_only_whitespace():
    assert make_upper("") == ""
    assert make_upper("   ") == ""

def test_make_upper_preserves_internal_whitespace_and_handles_uppercase():
    assert make_upper("  hello   world  ") == "HELLO   WORLD"
    assert make_upper("  HELLO  ") == "HELLO"

def test_make_upper_annotations_present():
    anns = make_upper.__annotations__
    assert 'string' in anns and 'return' in anns
    assert anns['string'] is str
    assert anns['return'] is str