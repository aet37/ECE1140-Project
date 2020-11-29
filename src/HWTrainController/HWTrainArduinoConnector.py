"""API for the HW Track Controller Module."""

from argparse import ArgumentParser
from enum import Enum
import socket
import sys
import logging
import polling
import serial
from src.SWTrainController.Controller import Controller
from time import sleep

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
    HWTRAIN_PULL_EBRAKE = 224
    HWTRAIN_SET_SETPOINT_SPEED = 225
    #PUT ALL MY REQUEST CODES HERE

class HWController(Controller):
    def __init__(self):
        self.arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)
        sleep(2)
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
