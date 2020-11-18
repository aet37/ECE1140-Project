# Created by Kenneth Meier
# Train implementation class

# SYSTEM INCLUDES
# (self, None)

# C++ PROJECT INCLUDES
# (self, None)
class Train:

    # The init method or constructor  
    def __init__(self, trainId):
        # Initialize vital variables

        # INTEGERS (self, Vital)
        self.m_destinationBlock = 0
        self.m_commandSpeed = 0
        self.m_currentSpeed = 0 # THIS IS CALCULATED
        self.m_position = 0 # THIS IS CALCULATED
        self.m_authority = 0
        self.m_currentLine = 0 # Default green line
        self.m_power = 0
        # INTEGERS (self, Nonvital)
        self.m_tempControl = 0

        # BOOLEANS (self, Vital)
        self.m_emergencyPassengeBrake = False
        self.m_serviceBrake = False
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
    
    ###############################################################
    # SETTERS AND GETTERS
    ###############################################################

    # DESTINATION BLOCK
    # @brief Setter function for destinationBlock
    # @param destinationBlock
    def SetDestinationBlock(self, destinationBlock):
        self.m_destinationBlock = destinationBlock

    # @brief gets destinationBlock
    # @return returns destinationBlock
    def GetDestinationBlock(self):
        return self.m_destinationBlock

    # COMMAND SPEED
    # @brief Setter function for Command Speed
    # @param commandSpeed
    def SetCommandSpeed(self, commandSpeed):
        self.m_commandSpeed = commandSpeed

    # @brief gets CommandSpeed
    # @return returns CommandSpeed
    def GetCommandSpeed(self):
        return self.m_commandSpeed

    # CURRENT SPEED
    # @brief Setter function for currentSpeed
    # @param currentSpeed
    def SetCurrentSpeed(self, currentSpeed):
        self.m_currentSpeed = currentSpeed

    # @brief gets currentSpeed
    # @return returns currentSpeed
    def GetCurrentSpeed(self):
        return self.m_currentSpeed

    # POSITION
    # @brief Setter function for position
    # @param position
    def SetPosition(self, position):
        self.m_position = position

    # @brief gets position
    # @return returns position
    def GetPosition(self):
        return self.m_position

    # AUTHORITY
    # @brief Setter function for authority
    # @param authority
    def SetAuthority(self, authority):
        self.m_authority = authority

    # @brief gets authority
    # @return returns authority
    def GetAuthority(self):
        return self.m_authority

    # CURRENT LINE
    # @brief Setter function for currentLine
    # @param currentLine
    def SetCurrentLine(self, currentLine):
        self.m_currentLine = currentLine

    # @brief gets currentLine
    # @return returns currentLine
    def GetCurrentLine(self):
        return self.m_currentLine

    # TEMP CONTROL
    # @brief Setter function for tempControl
    # @param tempControl
    def SetTempControl(self, tempControl):
        self.m_tempControl = tempControl

    # @brief gets tempControl
    # @return returns tempControl
    def GetTempControl(self):
        return self.m_tempControl

    # EMERGENCY PASSENGER BRAKE
    # @brief Setter function for emergencyPassengeBrake
    # @param emergencyPassengeBrake
    def SetEmergencyPassengeBrake(self, emergencyPassengeBrake):
        self.m_emergencyPassengeBrake = emergencyPassengeBrake

    # @brief gets emergencyPassengeBrake
    # @return returns emergencyPassengeBrake
    def GetEmergencyPassengeBrake(self):
        return self.m_emergencyPassengeBrake

    # SERVICE BRAKE
    # @brief Setter function for serviceBrake
    # @param serviceBrake
    def SetServiceBrake(self, serviceBrake):
        self.m_serviceBrake = serviceBrake

    # @brief gets serviceBrake
    # @return returns serviceBrake
    def GetServiceBrake(self):
        return self.m_serviceBrake

    # BRAKE COMMAND
    # ASK COLLIN ABOUT THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # What is the diff between service brake and brake command?
    # @brief Setter function for brakeCommand
    # @param brakeCommand
    def SetBrakeCommand(self, brakeCommand):
        self.m_brakeCommand = brakeCommand

    # @brief gets brakeCommand
    # @return returns brakeCommand
    def GetBrakeCommand(self):
        return self.m_brakeCommand

    # HEAD LIGHTS
    # @brief Setter function for headLights
    # @param headLights
    def SetHeadLights(self, headLights):
        self.m_headLights = headLights

    # @brief gets headLights
    # @return returns headLights
    def GetHeadLights(self):
        return self.m_headLights

    # CABIN LIGHTS
    # @brief Setter function for cabinLights
    # @param cabinLights
    def SetCabinLights(self, cabinLights):
        self.m_cabinLights = cabinLights

    # @brief gets cabinLights
    # @return returns cabinLights
    def GetCabinLights(self):
        return self.m_cabinLights

    # ADVERTISEMENTS
    # @brief Setter function for advertisements
    # @param advertisements
    def SetAdvertisements(self, advertisements):
        self.m_advertisements = advertisements

    # @brief gets advertisements
    # @return returns advertisements
    def GetAdvertisements(self):
        return self.m_advertisements

    # ANNOUNCEMENTS
    # @brief Setter function for announcements
    # @param announcements
    def SetAnnouncements(self, announcements):
        self.m_announcements = announcements

    # @brief gets announcements
    # @return returns announcements
    def GetAnnouncements(self):
        return self.m_announcements

    # DOORS
    # @brief Setter function for doors
    # @param doors
    def SetDoors(self, doors):
        self.m_doors = doors

    # @brief gets doors
    # @return returns doors
    def GetDoors(self):
        return self.m_doors

    # @brief gets currentBlock
    # @return returns currentBlock
    def GetCurrentBlock(self):
        return self.m_route.front()

    # @brief removes currentBlock
    def RemoveCurrentBlock(self):
        self.m_route.erase(self.m_route.begin())

    # POWER
    # @brief Setter function for power
    # @param power
    def SetPower(self, power):
        self.m_power = power

    # @brief gets power
    # @return returns power
    def GetPower(self):
        return self.m_power

    # TRAIN LENGTH
    # @brief Setter function for trainLength
    # @param trainLength
    def SetTrainLength(self, trainLength):
        self.m_trainLength = trainLength

    # @brief gets trainLength
    # @return returns trainLength
    def GetTrainLength(self):
        return self.m_trainLength

    # TRAIN WIDTH
    # @brief Setter function for trainWidth
    # @param trainLength
    def SetTrainWidth(self, trainWidth):
        self.m_trainWidth = trainWidth

    # @brief gets trainWidth
    # @return returns trainWidth
    def GetTrainWidth(self):
        return self.m_trainWidth

    # TRAIN HEIGHT
    # @brief Setter function for trainHeight
    # @param trainHeight
    def SetTrainHeight(self, trainHeight):
        self.m_trainHeight = trainHeight

    # @brief gets trainHeight
    # @return returns trainHeight
    def GetTrainHeight(self):
        return self.m_trainHeight

    # TRAIN MASS
    # @brief Setter function for trainMass
    # @param trainMass
    def SetTrainMass(self, trainMass):
        self.m_trainMass = trainMass

    # @brief gets trainMass
    # @return returns trainMass
    def GetTrainMass(self):
        return self.m_trainMass

    # TRAIN CREW COUNT
    # @brief Setter function for trainCrewCount
    # @param trainCrewCount
    def SetTrainCrewCount(self, trainCrewCount):
        self.m_trainCrewCount = trainCrewCount

    # @brief gets trainCrewCount
    # @return returns trainCrewCount
    def GetTrainCrewCount(self):
        return self.m_trainCrewCount

    # TRAIN PASS COUNT
    # @brief Setter function for trainPassCount
    # @param trainPassCount
    def SetTrainPassCount(self, trainPassCount):
        self.m_trainPassCount = trainPassCount

    # @brief gets trainPassCount
    # @return returns trainPassCount
    def GetTrainPassCount(self):
        return self.m_trainPassCount

    # SIGNAL PICKUP FAILURE
    # @brief Setter function for signalPickupFailure
    # @param signalPickupFailure
    def SetSignalPickupFailure(self, signalPickupFailure):
        self.m_signalPickupFailure = signalPickupFailure

    # @brief gets signalPickupFailure
    # @return returns signalPickupFailure
    def GetSignalPickupFailure(self):
        return self.m_signalPickupFailure

    # ENGINE FAILURE
    # @brief Setter function for engineFailure
    # @param engineFailure
    def SetEngineFailure(self, engineFailure):
        self.m_engineFailure = engineFailure

    # @brief gets engineFailure
    # @return returns engineFailure
    def GetEngineFailure(self):
        return self.m_engineFailure

    # BRAKE FAILURE
    # @brief Setter function for brakeFailure
    # @param brakeFailure
    def SetBrakeFailure(self, brakeFailure):
        self.m_brakeFailure = brakeFailure

    # @brief gets brakeFailure
    # @return returns brakeFailure
    def GetBrakeFailure(self):
        return self.m_brakeFailure

    # MODE
    # @brief Setter function for mode
    # @param mode
    def SetMode(self, mode):
        self.m_mode = mode

    # @brief gets mode
    # @return returns mode
    def GetMode(self):
        return self.m_mode

    # @brief Sets the train's route
    def SetRoute(self, route):
        self.m_route = route

    # @brief Gets the train's route
    def GetRoute(self):
        return self.m_route
