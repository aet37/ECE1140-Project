"""Unit test for the Lexer class"""

import sys
import pytest
sys.path.insert(1, '../../../..')
from src.SWTrackController.Compiler.lexer import CompilationError, Lexer, TokenType

# pylint: disable=misplaced-comparison-constant
def test_next_character():
    """Tests the next_character method

    PRECONDITIONS: Lexer made with input "test input"
    EXECUTION: Call next_character repeatedly
    POSTCONDITIONS: current_character matches character in "test input"
                    current_position increments once per call

    """
    test_input = "test input"
    lex = Lexer(test_input)
    assert test_input + '\n' == lex.source_code
    assert test_input[0] == lex.current_character
    assert lex.current_position == 0

    for i, char in enumerate(test_input[1:]):
        lex.next_character()

        assert char == lex.current_character
        assert (i + 1) == lex.current_position

    lex.next_character()
    assert '\n' == lex.current_character

    lex.next_character()
    assert '\0' == lex.current_character

def test_peek():
    """Tests the peek method

    PRECONDITIONS: Lexer made with input "test input"
    EXECUTION: lex.peek()
    POSTCONDITIONS: lex.peek returns 'e'
                    lex.current_character remains 't'

    """
    test_input = "test input"
    lex = Lexer(test_input)
    assert test_input[1] == lex.peek()
    assert test_input[0] == lex.current_character

def test_get_token_success():
    """Tests the get_token method

    PRECONDITIONS: Lexer made with input "TASK<PERIOD=10.50> myTask # This is my task"
    EXECUTION: lex.get_token() repeatedly
    POSTCONDITIONS: get_token() returns the correct token

    """
    test_input = "TASK<PERIOD=10.50> myTask # This is my task"
    lex = Lexer(test_input)

    token = lex.get_token()
    assert TokenType.TASK == token.type
    assert "TASK" == token.text

    token = lex.get_token()
    assert TokenType.OPEN_ANGLE == token.type
    assert "<" == token.text

    token = lex.get_token()
    assert TokenType.PERIOD == token.type
    assert "PERIOD" == token.text

    token = lex.get_token()
    assert TokenType.EQ == token.type
    assert "=" == token.text

    token = lex.get_token()
    assert TokenType.NUMBER == token.type
    assert "10.50" == token.text

    token = lex.get_token()
    assert TokenType.CLOSE_ANGLE == token.type
    assert ">" == token.text

    token = lex.get_token()
    assert TokenType.IDENTIFIER == token.type
    assert "myTask" == token.text

    token = lex.get_token()
    assert TokenType.NEWLINE == token.type
    assert "\n" == token.text

    token = lex.get_token()
    assert TokenType.EOF == token.type
    assert "" == token.text

def test_get_token_failure_1():
    """Tests the get_token method

    PRECONDITIONS: Lexer made with input "TASK<PERIOD=10.> myTask # This is my task"
    EXECUTION: lex.get_token() repeatedly
    POSTCONDITIONS: sys.exit is called

    """
    test_input = "TASK<PERIOD=10.> myTask # This is my task"
    lex = Lexer(test_input)

    lex.get_token()
    lex.get_token()
    lex.get_token()
    lex.get_token()

    with pytest.raises(CompilationError) as pytest_wrapped_e:
        lex.get_token()
    assert "Lexing error line #1 : Illegal character in number" == str(pytest_wrapped_e.value)

def test_get_token_failure_2():
    """Tests the get_token method

    PRECONDITIONS: Lexer made with input "TASK<PERIOD=10.50> my_Task # This is my task"
    EXECUTION: lex.get_token() repeatedly
    POSTCONDITIONS: sys.exit is called

    """
    test_input = "TASK<PERIOD=10.50> my_Task # This is my task"
    lex = Lexer(test_input)

    lex.get_token()
    lex.get_token()
    lex.get_token()
    lex.get_token()
    lex.get_token()
    lex.get_token()
    lex.get_token()

    with pytest.raises(CompilationError) as pytest_wrapped_e:
        lex.get_token()
    assert "Lexing error line #1 : Unknown token: _" == str(pytest_wrapped_e.value)


if __name__ == "__main__":
    raise Exception("Run using pytest")
