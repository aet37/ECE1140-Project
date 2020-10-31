"""Integration test for compiler"""

import sys
import pytest

sys.path.insert(1, '../../../../src/SWTrackController/Compiler')
from lexer import Lexer
from parse import Parser
from emitter import Emitter

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : There must be a single Main routine" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : There can only be one Main routine" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Referencing tag input2 before assignment" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Emitted event MissingEvent does not correspond to a task" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Routine MissingRoutine does not exist" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Too many end statements" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Missing matching ENDROUTINE" == pytest_wrapped_e.value.code

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        par.program()
    assert SystemExit == pytest_wrapped_e.type
    assert "Parsing error : Period below allowable limit 20" == pytest_wrapped_e.value.code

if __name__ == "__main__":
    raise Exception("Run using pytest")