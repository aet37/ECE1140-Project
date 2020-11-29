"""Module containing class pertaining to the plc program"""

from enum import Enum

class InstructionType(Enum):
    """Enumerated type for types of instructions"""
    XIC = 0
    XIO = 1
    OTE = 2
    OTL = 3
    OTU = 4

# pylint: disable=too-few-public-methods
class Instruction:
    """Class to represent a ladder logic instruction"""
    def __init__(self, instruction_type, argument):
        self.type = instruction_type
        self.argument = argument
