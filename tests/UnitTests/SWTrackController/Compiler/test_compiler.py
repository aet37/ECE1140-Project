"""Integration test for compiler"""

import sys
import pytest

sys.path.insert(1, '../../../../src')
from SWTrackController.Compiler.lexer import Lexer
from SWTrackController.Compiler.parse import Parser
from SWTrackController.Compiler.emitter import Emitter

# pylint: disable=misplaced-comparison-constant
def test_simple_program():
    """Tests the compilation of a simple program"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    par.program()

    assert par.emitter.requests == 'START_DOWNLOAD\n' \
                                   'CREATE_TAG input1 FALSE\n' \
                                   'CREATE_TAG output1 FALSE\n' \
                                   'CREATE_TASK PERIOD 1000 myTask\n' \
                                   'CREATE_ROUTINE Main\n' \
                                   'CREATE_RUNG\n' \
                                   'CREATE_INSTRUCTION XIO input1\n' \
                                   'CREATE_INSTRUCTION OTE output1\n' \
                                   'END_DOWNLOAD\n'

def test_missing_main():
    """Tests a program that is missing a main routine"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE myRoutine\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : There must be a single Main routine" == str(pytest_wrapped_e.value)

def test_multiple_mains():
    """Tests a program with multiple mains"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : There can only be one Main routine" == str(pytest_wrapped_e.value)

def test_no_tag():
    """Test program that uses a nonexistent tag"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input2\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : Referencing tag input2 before assignment" == str(pytest_wrapped_e.value)

def test_nonexistent_event():
    """Test program that uses a nonexistent event"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "EMIT MissingEvent\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : Emitted event MissingEvent does not " \
           "correspond to a task" == str(pytest_wrapped_e.value)

def test_nonexistent_routine():
    """Test program that jumps to a nonexistent routine"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "JSR MissingRoutine\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : Routine MissingRoutine does not exist" == str(pytest_wrapped_e.value)

def test_too_many_ends():
    """Test program that too many end statements"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : Too many end statements" == str(pytest_wrapped_e.value)

def test_missing_end():
    """Test program with missing ENDROUTINE"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : Missing matching ENDROUTINE" == str(pytest_wrapped_e.value)

def test_low_period():
    """Test program with a period less than 20ms"""
    code = "TAG input1 = FALSE\n" \
           "TAG output1 = FALSE\n" \
           "TASK<PERIOD=10> myTask\n" \
           "ROUTINE Main\n" \
           "RUNG\n" \
           "XIO input1\n" \
           "OTE output1\n" \
           "ENDRUNG\n" \
           "ENDROUTINE\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    with pytest.raises(Exception) as pytest_wrapped_e:
        par.program()
    assert "Parsing error : Period below allowable limit 20" == str(pytest_wrapped_e.value)

if __name__ == "__main__":
    raise Exception("Run using pytest")
