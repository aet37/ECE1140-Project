"""Module containing classes to communicate with the hw track controller"""

import threading
from enum import Enum
import serial

from src.SWTrackController.track_controller import TrackController
from src.UI.Common.common import DownloadInProgress
from src.logger import get_logger

logger = get_logger(__name__)

# Communications with controller
SERIAL_PORT = 'COM3'
RATE = 9600

class Code(Enum):
    """Codes to be sent to the arduino"""
    START_DOWNLOAD = 96 # Used by the gui to start a download
    END_DOWNLOAD = 97 # Used by the gui to end a download
    CREATE_TAG = 98 # Used by the gui to create a tag
    CREATE_TASK = 99 # Used by the gui to create a task
    CREATE_ROUTINE = 100 # Used by the gui to create a routine
    CREATE_RUNG = 101 # Used by the gui to create a rung
    CREATE_INSTRUCTION = 102 # Used by the gui to create an instruction
    SET_TAG_VALUE = 103 # Used by the gui to set a tag's value
    GET_TAG_VALUE = 104 # Used by the gui to get a tag's value
    GET_ALL_TAG_VALUES = 105 # Used by the gui to get all tag values

class HWTrackCtrlConnector(TrackController):
    """Class responsible for communicating with the hw track controller"""
    def __init__(self):
        self.arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)

        self.comms_lock = threading.Lock()

    def send_message(self, msg):
        """Writes the given message to the serial port

        :param str msg: Message to send
        """
        bytes_written = self.arduino.write(bytes(str(msg), 'utf-8'))
        logger.info("%s written to the controller", str(msg))

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
        """Reads the compiled program and downloads it to the controller

        :param file compiled_program: Path to the compiled PLC program
        """
        logger.debug("Downloading program %s", compiled_program)
        progress = DownloadInProgress()

        def _download_program():
            commands = []
            for line in open(compiled_program, 'r'):
                line = line.rstrip('\n')
                try:
                    space_index = line.index(' ')
                except ValueError:
                    space_index = len(line)

                # Construct the new line with the code replaced
                line = str(Code[line[:space_index]].value) + line[space_index:]
                commands.append(line)

            with self.comms_lock:
                for i, command in enumerate(commands):
                    self.send_message(command)
                    # No need for sleep here because of the get response
                    logger.info(self.get_response())
                    progress.progress_updated.emit((i + 1) / len(commands) * 100)

            progress.download_complete.emit()

        download_thread = threading.Thread(target=_download_program)
        download_thread.start()

        progress.exec()

    def get_tag_value(self, tag_name):
        """Gets a tag's value from inside the plc

        :param str tag_name: Name of the tag

        :return: Value of the tag
        :rtype: bool
        """
        self.send_message(" ".join((str(Code.GET_TAG_VALUE.value), tag_name)))
        response = self.get_response()
        if (len(response.split()) == 2):
            return bool(int(response.split()[1]))

    def set_tag_value(self, tag_name, value):
        """Sets a tag's value inside the plc

        :param str tag_name: Name of the tag
        :param bool value: Value to set to the tag to
        """
        self.send_message(" ".join(map(str, (Code.SET_TAG_VALUE.value, tag_name, int(value)))))
        logger.info(self.get_response())