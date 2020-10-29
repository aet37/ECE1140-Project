"""Integration test for compiler"""

import sys

sys.path.insert(1, '../../../../src/SWTrackController/Compiler')
from lexer import Lexer
from parse import Parser
from emitter import Emitter

def test_my_test():
    """
    
    """
    code = "TAG myTag = FALSE\n" \
           "XIO myTag\n" \
           "TASK<PERIOD=1000> myTask\n" \
           "ENDTASK\n"

    lex = Lexer(code)
    emit = Emitter('MyOutput')
    par = Parser(lex, emit)

    par.program()

    assert par.emitter.requests == 'START_DOWNLOAD\n' \
                                   'CREATE_TAG myTag FALSE\n' \
                                   'CREATE_INSTRUCTION XIO myTag\n' \
                                   'CREATE_TASK PERIOD 1000 myTask\n' \
                                   'END_DOWNLOAD\n'

if __name__ == "__main__":
    raise Exception("Run using pytest")