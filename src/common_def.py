"""Holds common definitions used throughout the train system"""

from enum import Enum

class Line(Enum):
    """Enumerated type for line color"""
    LINE_GREEN = 0
    LINE_RED = 1
    LINE_UNSPEC = 2


if __name__ == "__main__":
    raise Exception("Not to be run as a module")
