#
# Created by Collin Hough on 10.7.20
# Defines controller to be used on each train in system
#

# Defines the maximum power of the train engine
MAX_POWER = 120; # Units for max power are kW

# Define automatic to manual override password
PASSWORD = "override"

# Define sampling period for calculating power
T = 0.25

class Controller:

    # @brief initializes data coming from train model
    # @param com_sp = command speed
    # @param curr_sp = current speed
    # @param auth = authority
    def __init__(self, com_sp = 0, curr_sp = 0, auth = 0):
        # Safety critical information
        self.command_speed = com_sp
        self.current_speed = curr_sp
        self.setpoint_speed = 0
        self.power_command = 0
        self.authority = auth
        self.mode = False # 0 = Automatic, 1 = Manual
        self.serviceBrake = False
        self.emergencyBrake = False

        # Train Engineer inputs
        self.kp = 0
        self.ki = 0

        # Variables for power calculation
        self.uk = 0
        self.uk1 = 0
        self.ek = 0
        self.ek1 = 0

        # NonVital Operations (0 = ON, 1 = OFF)
        self.doors = 0
        self.announcements = 0
        self.lights = 0
        self.temperature = 0
        self.advertisements = 0

        # Failure cases
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False

        # Struct which holds all non-vital operations
        #NonVitalOperations NVO

    ###############################/
    # SETTERS AND GETTERS
    ###############################/

    # @brief Setter function for Kp
    # @param KP = kp
    def setKp(self, KP):
        self.kp = KP

    # @brief Setter function for Ki
    # @param KI = ki
    def setKi(self, KI):
        self.ki = KI

    # @brief Setter function for command speed
    # @param com_sp == command_speed
    def setCommandSpeed(self, com_sp):
        self.command_speed = com_sp

    # @brief Setter function for current speed
    # @param curr_sp == current_speed
    def setCurrentSpeed(self, curr_sp):
        self.current_speed = curr_sp

    # @brief Setter function for setpoint speed
    # @param setp_sp == setpoint speed
    def setSetpointSpeed(self, setp_sp):
        self.setpoint_speed = setp_sp

    # @brief Setter function for authority
    # @param auth == authority
    def setAuthority(self, auth):
        self.authority = auth

    # @brief Getter function for command speed
    # @return command_speed
    def getCommandSpeed(self):
        return self.command_speed

    # @brief Getter function for current speed
    # @return current_speed
    def getCurrentSpeed(self):
        return self.current_speed

    # @brief Getter function for setpoint speed
    # @return setpoint speed
    def getSetpointSpeed(self):
        return self.setpoint_speed

    # @brief Getter function for authority
    # @return authority
    def getAuthority(self):
        return self.authority

    # @brief Getter function for power command
    # @return power_command
    def getPowerCommand(self):
        return self.power_command

    # @brief Getter function for mode
    # @return mode
    def getMode(self):
        return self.mode

    # @brief Getter function for service brake
    # @return service brake
    def getServiceBrake(self):
        return self.serviceBrake

    # NON-VITAL GETTERS

    # @brief open/close doors
    # @return doors
    def getDoors(self):
        return self.doors

    # @brief turn lights on/off
    # @ return lights
    def getLights(self):
        return self.lights

    # @brief turn announcements on/off
    # @return announcements
    def getAnnounceStations(self):
        return self.announcements

    # @brief turn advertisements on/off
    # @return advertisements
    def getAds(self):
        return self.advertisements

    ###############################/
    # VITAL OPERATIONS
    ###############################/
    #
    # @brief calculates power command that will be sent to train model
    #/
    def calculatePower(self):
        # Find Verror depending on mode
        Verror = 0
        if self.mode == 0: # Automatic Mode
            Verror = self.command_speed - self.current_speed
        else: # Manual Mode
            Verror = self.setpoint_speed - self.current_speed

        # Set ek as the kth sample of velocity error
        self.ek = Verror

        # Determine uk as shown in slide 65 of lecture 2
        if self.power_command < MAX_POWER:
            # Find uk 
            self.uk = self.uk1 + (T/2) * (self.ek + self.ek1)
        else:
            self.uk = self.uk1
   
        # Find power command
        self.power_command = (self.kp * self.ek) + (self.ki * self.uk)

        # Set past values of uk and ek
        self.uk1 = self.uk
        self.ek1 = self.ek


    # @brief ensures train does not exceed speed limit
    # @brief if train is in automatic mode, speed is set to command speed
    # @brief if train is in manual mode, speed is set to setpoint speed
    # void regulateSpeed() IDK IF I NEED THIS

    # @brief safety critical aspect to stop train immediately
    # @return active emergency brake
    def activateEmergencyBrake(self):
        self.emergencyBrake = True

    # @brief safety critical aspect to reset emergency brake
    # @return off emergency brake
    def resetEmergencyBrake(self):
        self.emergencyBrake = False

    # @brief toggle service brake on and off
    # @return toggled service brake
    def toggleServiceBrake(self):
        self.serviceBrake = not self.serviceBrake
    
    # @brief allows operator to switch between manual and automatic mode
    # @param override = string code entered by operator to initiate manual override
    # @return returns boolean value to signify if override was successful
    def toggleMode(self, override):
        # Check if override code is correct
        if override == PASSWORD:
            self.mode = not self.mode
            return self.mode
        else:
            return False

    ###############################/
    # NON-VITAL OPERATIONS
    ###############################/
    
    # @brief open/close doors
    # @return toggled doors
    def toggleDoors(self):
        self.doors = not self.doors
        return self.doors
    
    # @brief turn lights on/off
    # @return toggled lights
    def toggleLights(self):
        self.lights = not self.lights
        return self.lights
    
    # @brief turn announcements on/off
    # @return toggled announcements
    def announceStations(self):
        self.announcements = not self.announcements
        return self.announcements
    
    # @brief turn advertisements on/off
    # @return toggled advertisements
    def toggleAds(self):
        self.advertisements = not self.advertisements
        return self.advertisements
    
    # @brief sets temperature of train cabin
    # @param temp = temperature cabin is set to
    def setCabinTemp(self, temp):
        self.temperature = temp
    
    # @brief gets temperature of train cabin
    # @return returns temperature of cabin
    def getCabinTemp(self):
        return self.temperature

#endif