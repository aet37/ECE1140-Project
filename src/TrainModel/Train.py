# Created by Kenneth Meier
# Train implementation class

# SYSTEM INCLUDES
# (self, None)

# PYTHON PROJECT INCLUDES
from src.common_def import *
class Train:

    # The init method or constructor  
    def __init__(self, trainId):
        # Initialize vital variables

        # INTEGERS (self, Vital)
        self.m_destinationBlock = 0
        self.m_commandSpeed = 0.0
        self.m_currentSpeed = 0.0 # THIS IS CALCULATED
        self.m_position = 0.0 # THIS IS CALCULATED
        self.m_acceleration = 0.0 # THIS IS CALCULATED (ALWAYS IN m/s)
        self.m_authority = False
        self.m_currentLine = Line.LINE_GREEN # Default green line
        self.m_power = 0.0
        # INTEGERS (self, Nonvital)
        self.m_tempControl = 0.0

        # BOOLEANS (self, Vital)
        self.m_emergencyPassengerBrake = False
        self.m_serviceBrake = True
        self.m_brakeCommand = False
        # BOOLEANS (self, Nonvital)
        self.m_headLights = False
        self.m_cabinLights = False
        self.m_advertisements = False
        self.m_announcements = False
        self.m_doors = False

        # Parameter Inputs
        self.m_trainLength = 32.2 # Meters
        self.m_trainWidth = 2.65 # Meters
        self.m_trainHeight = 3.42 # Meters
        self.m_trainMass = 40.9 # Tons
        self.m_trainCrewCount = 2 # HARDCODED (self, Unless told otherwise)
        self.m_trainPassCount = 0

        # Failure cases
        self.m_signalPickupFailure = False
        self.m_engineFailure = False
        self.m_brakeFailure = False

        # MISC.
        self.m_mode = False  # Auto or Manuel
        self.m_route = []
    