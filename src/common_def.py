"""Holds common definitions used throughout the train system"""

from enum import Enum

class Line(Enum):
    """Enumerated type for line color"""
    LINE_GREEN = 0
    LINE_RED = 1
    LINE_UNSPEC = 2

def pairwise(iterable):
    """Function used to iterate a list two elements at a time"""
    a = iter(iterable)
    return zip(a, a)


if __name__ == "__main__":
    raise Exception("Not to be run as a module")
