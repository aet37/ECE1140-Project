"""
    Author: Collin Hough

    Date: 10.7.20
"""
from src.common_def import Converters

# Defines the maximum power of the train engine
MAX_POWER = 120000 # Units for max power are kW

# Define automatic to manual override password
PASSWORD = "override"

# Define sampling period for calculating power (1/10th of a second)
T = 0.2

class Controller:
    """ Defines controller to be used on each train """

    def __init__(self, com_sp = 0, curr_sp = 0, auth = 0):
        """
            Initializes data coming from train model
            com_sp = command speed
            curr_sp = current speed
            auth = authority
        """
        # Safety critical information
        self.command_speed = com_sp
        self.current_speed = curr_sp
        self.setpoint_speed = 0.0
        self.power_command = 0.0
        self.authority = auth
        self.mode = False # 0 = Automatic, 1 = Manual
        self.service_brake = True
        self.emergency_brake = False

        # Train Engineer inputs
        self.kp = 0.0
        self.ki = 0.0

        # Variables for power calculation
        self.uk = 0.0
        self.uk1 = 0.0
        self.ek = 0.0
        self.ek1 = 0.0

        # NonVital Operations (0 = ON, 1 = OFF)
        self.doors = 0
        self.announcements = 0
        self.lights = 0
        self.temperature = 70
        self.advertisements = 0

        # Failure cases
        self.signal_pickup_failure = False
        self.engine_failure = False
        self.brake_failure = False

        # Used for starting and stopping the train's power loop
        self.hold_power_loop = False

    ###############################/
    # VITAL OPERATIONS
    ###############################/

    def calculate_power(self):
        """
            Calculates power command that will be sent to train model
            Units:
                Kp: (W / (m/s) )
                Ki: (W / m)
                Command Speed: m/s
                Current Speed: m/s
                Setpoint Speed: m/s
                ek/ek1: m/s
                uk/uk1: m
        """
        # Convert Command Speed, Current Speed, and Setpoint Speed into m/s
        self.convert_command_speed = self.command_speed * Converters.KmHr_to_mps
        self.convert_current_speed = self.current_speed * Converters.MPH_to_mps
        self.convert_setpoint_speed = self.setpoint_speed * Converters.MPH_to_mps

        # Find Verror depending on mode
        velocity_error = 0
        if self.mode == 0: # Automatic Mode
            velocity_error = self.convert_command_speed - self.convert_current_speed
        else: # Manual Mode
            velocity_error = self.convert_setpoint_speed - self.convert_current_speed

        # Set ek as the kth sample of velocity error
        self.ek = velocity_error

        # Determine uk as shown in slide 65 of lecture 2
        if self.power_command < MAX_POWER:
            # Find uk
            self.uk = self.uk1 + (T/2) * (self.ek + self.ek1)
        else:
            self.uk = self.uk1

        # Check for engine failure
        if self.power_command > 0 and self.current_speed == 0:
            self.engine_failure == True

        # Find power command
        if self.service_brake == True or self.emergency_brake == True:
            self.power_command = 0
            self.uk = 0
            self.ek = 0
        else:
            self.power_command = (self.kp * self.ek) + (self.ki * self.uk)
            # Cut off power at appropriate limits
            if(self.power_command > 120000):
                self.power_command = 120000
            elif(self.power_command < -120000):
                self.power_command = -120000

        # Set past values of uk and ek
        self.uk1 = self.uk
        self.ek1 = self.ek


    # @brief ensures train does not exceed speed limit
    # @brief if train is in automatic mode, speed is set to command speed
    # @brief if train is in manual mode, speed is set to setpoint speed
    # void regulateSpeed() IDK IF I NEED THIS

    def activate_emergency_brake(self):
        """ Safety critical aspect to stop train immediately """
        self.emergency_brake = True

    def reset_emergency_brake(self):
        """ Safety critical aspect to reset emergency brake """
        self.emergency_brake = False

    def toggle_service_brake(self):
        """ Toggle service brake on and off """
        # Check for potential failure
        if self.service_brake == True:
            if self.brake_failure == True:
                # If brake failure occurs do not change service brake
                self.service_brake = True
            else:
                # If no brake failure toggle brake normally
                self.service_brake = not self.service_brake
        else:  
            self.service_brake = not self.service_brake

    def toggle_mode(self, override):
        """ Allows operator to switch between manual and automatic mode """
        # Check if override code is correct
        if override == PASSWORD:
            self.mode = not self.mode

    ###############################/
    # NON-VITAL OPERATIONS
    ###############################/

    def toggle_doors(self):
        """ Open/close doors """
        self.doors = not self.doors

    def toggle_lights(self):
        """ Turn lights on/off """
        self.lights = not self.lights

    def toggle_announcements(self):
        """ Turn announcements on/off """
        self.announcements = not self.announcements

    def toggle_ads(self):
        """ Turn advertisements on/off """
        self.advertisements = not self.advertisements
