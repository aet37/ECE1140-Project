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
            if (key == "lights"):
                if self.lights != bool(int(value)):
                    self.lights = bool(int(value))
                    signals.train_model_gui_receive_lights.emit(0, self.lights)
            # make other if statements here for other variables.
            # get non-vitals working first
            # need someway to tell if the power and speed change to display on arduino

        if HWController.run_timer:
            self.timer = threading.Timer(TIMER_PERIOD, self.get_data)
            self.timer.start()

    def __init__(self, com_sp = 0, curr_sp = 0, auth = 0):
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
