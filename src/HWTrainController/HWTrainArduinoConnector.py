"""API for the HW Track Controller Module."""

from argparse import ArgumentParser
from time import sleep
from enum import Enum
import socket
import sys
import logging
import polling
import serial
from src.signals import signals
import threading
from src.common_def import pairwise
from src.SWTrainController.Controller import Controller

logger = logging.getLogger(__name__)

#CONTINUALLY PING THE ARDRUINO TO GET BUTTON PRESSES

#First train dispatched, creates my controller
#Make python class that inherits from Collins controller class that then communicated with the arduino
#From src.SWTrainController.Controller import Controller
#HWController(Controller) to inhereit
#Make a sens message for each function that needs to go to the arduino

# Communications with controller
SERIAL_PORT = 'COM6'
RATE = 9600

class Codes(Enum):
    # HWTRAIN_PULL_EBRAKE = 224
    # HWTRAIN_SET_SETPOINT_SPEED = 225
    # HWTRAIN_PRESS_SERVICE_BRAKE = 226
    # HWTRAIN_TOGGLE_DAMN_DOORS = 227
    # HWTRAIN_TOGGLE_CABIN_LIGHTS = 228
    # HWTRAIN_SET_TEMPERATURE = 229
    # HWTRAIN_ANNOUNCE_STATIONS = 230
    # HWTRAIN_DISPLAY_ADS = 231
    # HWTRAIN_DISPATCH_TRAIN = 235
    # HWTRAIN_UPDATE_CURRENT_SPEED = 236
    # HWTRAIN_UPDATE_COMMAND_SPEED = 237
    # HWTRAIN_UPDATE_AUTHORITY = 238
    # HWTRAIN_SIGNAL_FAILURE = 239
    # HWTRAIN_PULL_PASSENGER_EBRAKE = 240
    # HWTRAIN_GUI_GATHER_DATA = 241
    # HWTAIN_ENGINE_FAILURE = 242
    # HWTRAIN_GUI_SET_KP = 243
    # HWTRAIN_GUI_GET_MODE = 244
    # HWTRAIN_GUI_DISPLAY_POWER = 245
    # HWTRAIN_GUI_SET_KI = 246
    # HWTRAIN_BRAKE_FAILURE = 247
    HWTRAIN_GET_DATA = 248
    HWTRAIN_SEND_SIGFAIL_DATA = 249
    HWTRAIN_SEND_ENGFAIL_DATA = 250
    HWTRAIN_SEND_BRAKEFAIL_DATA = 251
    HWTRAIN_SEND_POWER_DATA = 252
    HWTRAIN_SEND_SETSP_DATA = 253

TIMER_PERIOD = 2

class HWController(Controller):

    run_timer = True

    def get_data(self):
        print("A")
        #send_message(RequestCode.HWTRAIN_SET_TEMPERATURE, "50")
        self.send_message("{}".format(Codes.HWTRAIN_GET_DATA.value))
        tag_values = str(self.get_response()).rstrip('\'')
        splits = tag_values.split(" ")
        print(tag_values)
        for key, value in pairwise(splits[1:]):
            print("Key")
            print (key)
            
            if (key == "ebrake"):
                if self.emergency_brake != bool(int(value)):
                    self.emergency_brake = bool(int(value))
                    signals.train_model_gui_receive_ebrake.emit(0, self.emergency_brake)
            if (key == "brake"):
                if self.service_brake != bool(int(value)):
                    self.service_brake = bool(int(value))
                    signals.train_model_gui_receive_service_brake.emit(0, self.service_brake)
            if (key == "doors"):
                if self.doors != bool(int(value)):
                    self.doors = bool(int(value))
                    signals.train_model_gui_receive_doors.emit(0, self.doors)
            if (key == "lights"):
                if self.lights != bool(int(value)): # to make sure that there was a change from the hardware to the gui
                    self.lights = bool(int(value))
                    signals.train_model_gui_receive_lights.emit(0, self.lights)
            if (key == "ads"):
                if self.advertisements != bool(int(value)):
                    self.advertisements = bool(int(value))
                    signals.train_model_gui_receive_ads.emit(0, self.advertisements)
            if (key == "announce"):
                if self.announcements != bool(int(value)):
                    self.announcements = bool(int(value))
                    signals.train_model_gui_receive_announce_stations.emit(0, self.announcements)
            if (key == "sigfail"):
                if (self.authority == None):
                    if (self.command_speed == None):
                        if(self.signal_pickup_failure == True):
                            self.send_message("{} {}".format(Codes.HWTRAIN_SEND_SIGFAIL_DATA.value, self.signal_pickup_failure))
            if (key == "engfail"):
                if (1): #past speed < current speed):
                    if (1):#engine failure == True):
                        # display engine failure
                        self.send_message("{} {}".format(Codes.HWTRAIN_SEND_ENGFAIL_DATA.value, self.engine_failure))
            if (key == "brakefail"):
                if (self.service_brake==True):
                    if(self.brake_failure==True):
                        self.send_message("{} {}".format(Codes.HWTRAIN_SEND_BRAKEFAIL_DATA.value, self.brake_failure))
            if (key == "temp"):
                if self.temperature != int(value):
                    self.temperature = int(value)
                    signals.train_model_gui_receive_sean_paul.emit(0, self.temperature)
            if (key == "speed"):
                if self.command_speed != int(value):
                    self.command_speed = int(value)
                    signals.train_model_update_command_speed.emit(0, self.command_speed)
            if (key == "kp"):
                self.kp = int(value)
            if (key == "ki"):
                self.ki = int(value)
        print("KP: " + str(self.kp))
        print("KI: " + str(self.ki))
        print("Command Speed: " + str(self.command_speed))

            # def toggle_service_brake(self):
            #     """ Toggle service brake on and off """
            #     # Check for potential failure
            #     if self.service_brake == True:
            #         if self.brake_failure == True:
            #             # If brake failure occurs do not change service brake
            #             self.service_brake = True
            #         else:
            #             # If no brake failure toggle brake normally
            #             self.service_brake = not self.service_brake
            #     else:  
            #         self.service_brake = not self.service_brake


            # make other if statements here for other variables.
            # get non-vitals working first
            # need someway to tell if the power and speed change to display on arduino

        # send message to arduino with what need be displayed
        # self.send_message("{} {}".format(Codes.HWTRAIN_SEND_POWER_DATA.value, self.power_command))
        # self.send_message("{} {}".format(Codes.HWTRAIN_SEND_SETSP_DATA.value, self.setpoint_speed))
        # self.send_message("{} {}".format(Codes.HWTRAIN_SEND_SIGFAIL_DATA.value, self.signal_pickup_failure))
        # self.send_message("{} {}".format(Codes.HWTRAIN_SEND_BRAKEFAIL_DATA.value, self.brake_failure))
        # self.send_message("{} {}".format(Codes.HWTRAIN_SEND_ENGFAIL_DATA.value, self.engine_failure))
        if HWController.run_timer:
            self.timer = threading.Timer(TIMER_PERIOD, self.get_data)
            self.timer.start()

    def __init__(self, com_sp = 0, curr_sp = 0, auth = 0):

        super().__init__(com_sp, curr_sp, auth)
        print("COmmand: " + str(com_sp))
        # # Safety critical information
        # self.command_speed = com_sp
        # self.current_speed = curr_sp
        # self.setpoint_speed = 0.0
        # self.power_command = 0.0
        # self.authority = auth
        # self.mode = False # 0 = Automatic, 1 = Manual
        # self.service_brake = True
        # self.emergency_brake = False

        # # Train Engineer inputs
        # self.kp = 0.0
        # self.ki = 0.0

        # # Variables for power calculation
        # self.uk = 0.0
        # self.uk1 = 0.0
        # self.ek = 0.0
        # self.ek1 = 0.0

        # # NonVital Operations (0 = ON, 1 = OFF)
        # self.doors = 0
        # self.announcements = 0
        # self.lights = 0
        # self.temperature = 70
        # self.advertisements = 0

        # # Used for starting and stopping the train's power loop
        # self.hold_power_loop = False

        # # Failure cases
        # self.signal_pickup_failure = False
        # self.engine_failure = False
        # self.brake_failure = False
        self.arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)
        sleep(2)
        self.timer = threading.Timer(TIMER_PERIOD, self.get_data)
        
        self.timer.start()
        
    def send_message(self, msg):
        """Writes the given message to the serial port

        :param str msg: Message to send
        """
        bytes_written = self.arduino.write(bytes(str(msg), 'utf-8'))
        logger.info("%d bytes written to the controller", bytes_written)

    def get_response(self):
        """Gets the response from the controller.
        :return: Response of the controller to the previous request
        :rtype: bytes
        """
        self.arduino.flushInput()
        response = self.arduino.readline()
        logger.info("Response from controller %s", response)
        # Remove \r\n from the end of the response
        return response.rstrip(b'\t\r\n ')
