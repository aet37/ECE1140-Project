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
    avg_person_tons = 0.089

class TrackCircuit:
    """Class to hold attributes of track circuit"""
    def __init__(self, command_speed: float, authority: bool):
        self.command_speed = command_speed
        self.authority = authority

class Beacon:
    """Class to hold attributes of beacon"""
    def __init__(self):
        self.station_name = ""
        self.service_brake = False
        self.DoorSide = None
        self.lastStation = False

class DoorSide(Enum):
    """Class to tell train model which door sides to open"""
    SIDE_RIGHT = 0
    SIDE_LEFT = 1
    SIDE_BOTH = 2


if __name__ == "__main__":
    raise Exception("Not to be run as a module")
