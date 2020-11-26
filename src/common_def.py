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

class Converters:
    """Enumerated type for converter"""
    KmHr_to_mps = 0.277778
    MPH_to_mps = 0.44704
    mps_to_MPH = 2.23694
    KmHr_to_MPH = 0.621371
    Tons_to_kg = 907.1850030836
    mps_to_KmHr = 3.6

class TrackCircuit:
    """Class to hold attributes of track circuit"""
    command_speed = 0
    authority = 0


if __name__ == "__main__":
    raise Exception("Not to be run as a module")
