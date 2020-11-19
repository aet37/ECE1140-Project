"""Module containing classes to communicate with the hw track controller"""

from time import sleep
import logging
import serial
import threading
from serial.serialutil import SerialException
from enum import Enum

logger = logging.getLogger(__name__)

# Communications with controller
SERIAL_PORT = 'COM3'
RATE = 9600

class Code(Enum):
    START_DOWNLOAD = 96 # Used by the gui to start a download
    END_DOWNLOAD = 97 # Used by the gui to end a download
    CREATE_TAG = 98 # Used by the gui to create a tag
    CREATE_TASK = 99 # Used by the gui to create a task
    CREATE_ROUTINE = 100 # Used by the gui to create a routine
    CREATE_RUNG = 101 # Used by the gui to create a rung
    CREATE_INSTRUCTION = 102 # Used by the gui to create an instruction
    SET_TAG_VALUE = 103 # Used by the gui to set a tag's value
    GET_TAG_VALUE = 104 # Used by the gui to get a tag's value

class HWTrackCtrlConnector:
    """Class responsible for communicating with the hw track controller"""
    def __init__(self):
        try:
            self.arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)
            sleep(2)
        except SerialException:
            print("No arduino")

        self.comms_lock = threading.Lock()

    def send_message(self, msg):
        """Writes the given message to the serial port

        :param str msg: Message to send
        """
        print(msg)
        bytes_written = self.arduino.write(msg)
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

    def download_program(self, compiled_program):
        """"""
        with self.comms_lock:
            for line in open(compiled_program, 'r'):
                line = line.rstrip('\n')
                try:
                    spaceIndex = line.index(' ')
                except ValueError:
                    spaceIndex = len(line)

                # Construct the new line with the code replaced
                line = str(Code[line[:spaceIndex]].value) + line[spaceIndex:]

                self.send_message(bytes(line, 'utf-8'))
                sleep(0.2)
                logger.info(self.get_response())
