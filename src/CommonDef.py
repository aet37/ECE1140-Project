"""
	@file CommonDef.py

	@purpose Hold common definitions used throughout the train system

	@date 11.16.2020

"""

from enum import Enum

"""
    @enum Line
    
    @brief Enumerated type telling line or train

    @li LINE_GREEN
    @li LINE_RED
    @li LINE_UNSPEC
"""

class Line(Enum):
	LINE_GREEN = 0
	LINE_RED = 1
	LINE_UNSPEC = 2


# Do Not allow to be run as Main Module
if __name__ == "__main__":
	raise Exception("Not to be run as a module")