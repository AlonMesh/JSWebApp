import pytest
from server.utils.match import normalize_code, is_solution_match

def test_normalize_code():
    # Test removing empty lines and stripping whitespace
    code = "   def foo():\n\n    return 42  \n\n"
    expected = "def foo():\nreturn 42"
    assert normalize_code(code) == expected

    # Test code with no changes needed
    code = "def bar():\n    return 24"
    expected = "def bar():\nreturn 24"
    assert normalize_code(code) == expected

    # Test completely empty input
    code = ""
    expected = ""
    assert normalize_code(code) == expected

    # Test input with only whitespace
    code = "   \n   \n"
    expected = ""
    assert normalize_code(code) == expected

def test_is_solution_match():
    # Test matching code
    code = "   def foo():\n    return 42  \n"
    solution = "def foo():\nreturn 42"
    assert is_solution_match(code, solution) is True

    # Test non-matching code
    code = "def foo():\n    return 42"
    solution = "def foo():\n    return 24"
    assert is_solution_match(code, solution) is False

    # Test matching with extra whitespace
    code = "   def foo():\n\n    return 42  \n\n"
    solution = "def foo():\nreturn 42"
    assert is_solution_match(code, solution) is True

    # Test one empty and one non-empty input
    code = ""
    solution = "def foo():\nreturn 42"
    assert is_solution_match(code, solution) is False
    
    # Test with // docs in the middle of the code
    code = "def foo(): // doc1 doc2\n    // doc3\n    return 42"
    solution = "def foo():\nreturn 42"
    assert is_solution_match(code, solution) is True