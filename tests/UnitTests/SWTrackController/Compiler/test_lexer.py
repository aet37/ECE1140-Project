"""Unit test for the Lexer class"""

import sys
sys.path.insert(1, '../../../../src/SWTrackController/Compiler')
from Lexer import Lexer

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

    PRECONDITIONS: Lexer made input "test input"
    EXECUTION: lex.peek()
    POSTCONDITIONS: lex.peek returns 'e'
                    lex.current_character remains 't'
    
    """
    test_input = "test input"
    lex = Lexer(test_input)
    assert test_input[1] == lex.peek()
    assert test_input[0] == lex.current_character


if __name__ == "__main__":
    raise Exception("Run using pytest")
