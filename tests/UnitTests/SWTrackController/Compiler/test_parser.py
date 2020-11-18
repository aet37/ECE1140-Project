"""Unit test for the Parser class"""

import sys
from mock import MagicMock
import pytest

sys.path.insert(1, '../../../..')
from src.SWTrackController.Compiler.parse import Parser
from src.SWTrackController.Compiler.lexer import Lexer, CompilationError
from src.SWTrackController.Compiler.emitter import Emitter

# pylint: disable=redefined-outer-name
@pytest.fixture(scope='function')
def mock_emitter():
    """Creates a mock emitter to use"""
    return MagicMock(Emitter)

# pylint: disable=misplaced-comparison-constant
def test_statement_tag_1(mock_emitter):
    """Test the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "TAG myTag = TRUE\nTAG myTag = FALSE"
    par = Parser(Lexer(source_code), mock_emitter)
    par.program()

def test_statement_tag_2(mock_emitter):
    """Test the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: Exception is thrown with correct error message

    """
    source_code = "TAG myTag = notAKeyword"
    par = Parser(Lexer(source_code), mock_emitter)

    with pytest.raises(CompilationError) as pytest_wrapped_e:
        par.program()
    assert "Parsing error line #2 : Expected FALSE, but found notAKeyword" == str(pytest_wrapped_e.value)

def test_statement_task_1(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "TASK<PERIOD=1000> myTask"
    par = Parser(Lexer(source_code), mock_emitter)

    par.statement()

def test_statement_task_2(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "TASK<EVENT=myEvent> myTask"
    par = Parser(Lexer(source_code), mock_emitter)

    par.statement()

def test_statement_task_3(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: Exception is thrown with correct error message

    """
    source_code = "TASK<CONTINUOUS> myTask"
    par = Parser(Lexer(source_code), mock_emitter)

    with pytest.raises(CompilationError) as pytest_wrapped_e:
        par.statement()
    assert "Parsing error line #1 : Invalid task type CONTINUOUS" == str(pytest_wrapped_e.value)

def test_statement_routine_success(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "ROUTINE Main"
    par = Parser(Lexer(source_code), mock_emitter)
    par.stack.append('TASK')

    par.statement()

def test_statement_routine_failure(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: Exception is thrown

    """
    source_code = "ROUTINE "
    par = Parser(Lexer(source_code), mock_emitter)
    par.stack.append('TASK')

    with pytest.raises(CompilationError) as pytest_wrapped_e:
        par.statement()
    assert "Parsing error line #2 : Expected IDENTIFIER, but found \n" == str(pytest_wrapped_e.value)

def test_statement_rung_1(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "RUNG"
    par = Parser(Lexer(source_code), mock_emitter)
    par.stack.append('ROUTINE')

    par.statement()

def test_statement_rung_2(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "RUNG myRung"
    par = Parser(Lexer(source_code), mock_emitter)
    par.stack.append('ROUTINE')

    par.statement()

def test_statement_instructions(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "XIC tag\nXIO tag\nOTE tag\nOTL tag\nOTU tag\nJSR routine\nEMIT event\nRET"
    par = Parser(Lexer(source_code), mock_emitter)

    # Add tag to the symbols to avoid errors
    par.tags.add('tag')
    par.events.add('event')
    par.routines.add('routine')

    par.program()

def test_statement_end(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "ENDRUNG\nENDROUTINE\nENDTASK"
    par = Parser(Lexer(source_code), mock_emitter)
    par.stack.append('TASK')
    par.stack.append('ROUTINE')
    par.stack.append('RUNG')
    par.main_flag = True

    par.program()

if __name__ == "__main__":
    raise Exception("Run with pytest")
