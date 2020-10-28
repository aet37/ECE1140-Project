"""Unit test for the Parser class"""

import sys
from mock import MagicMock
import pytest

sys.path.insert(1, '../../../../src/SWTrackController/Compiler')
from parse import Parser
from lexer import Lexer
from emitter import Emitter

@pytest.fixture(scope='function')
def mock_emitter(monkeypatch):
    monkeypatch.setattr('emitter.Emitter', MagicMock(Emitter))
    return Emitter


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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Expected FALSE, but found notAKeyword" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.statement()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Invalid task type CONTINUOUS" == pytest_wrapped_e.value.code

def test_statement_routine_success(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "ROUTINE Main"
    par = Parser(Lexer(source_code), mock_emitter)

    par.statement()

def test_statement_routine_failure(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: Exception is thrown

    """
    source_code = "ROUTINE "
    par = Parser(Lexer(source_code), mock_emitter)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.statement()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Expected IDENTIFIER, but found \n" == pytest_wrapped_e.value.code

def test_statement_rung_1(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "RUNG"
    par = Parser(Lexer(source_code), mock_emitter)

    par.statement()

def test_statement_rung_2(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "RUNG myRung"
    par = Parser(Lexer(source_code), mock_emitter)

    par.statement()

def test_statement_instructions(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "XIC tag\nXIO tag\nOTE tag\nOTL tag\nOTU tag\nJSR routine\nEMIT event\nRET"
    par = Parser(Lexer(source_code), mock_emitter)

    par.program()

def test_statement_end(mock_emitter):
    """Tests the statement method

    PRECONDITIONS: Create parser with line source_code
    EXECUTION: par.statement()
    POSTCONDITION: No exception is thrown

    """
    source_code = "ENDRUNG\nENDROUTINE\nENDTASK"
    par = Parser(Lexer(source_code), mock_emitter)

    par.program()

if __name__ == "__main__":
    raise Exception("Run with pytest")
