# Created by Kenneth Meier
# Block implementation class

# SYSTEM INCLUDES
# (self, None)

# C++ PROJECT INCLUDES
from src.common_def import *
class Block:

    # The init method or constructor  
    def __init__(self, blockId):
        # Initialize vital variables
        # INTEGERS (self, Vital)
        self.m_elevation = 0
        self.m_slope = 0
        self.m_sizeOfBlock = 0 
        self.m_accelerationLimit = 0
        self.m_decelerationLimit = 0
        self.m_speedLimit = 0
        self.m_travelDirection = 0
        self.m_station = False
        self.beacon1 = None
        self.beacon2 = None
