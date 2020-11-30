"""Module containing classes to communicate with the hw track controller"""

import threading
from enum import Enum
import serial

from src.common_def import pairwise
from src.SWTrackController.track_controller import TrackController
from src.UI.Common.common import DownloadInProgress
from src.signals import signals
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

TIMER_PERIOD = 1.6

class HWTrackCtrlConnector(TrackController):
    """Class responsible for communicating with the hw track controller"""

    run_timer = True

    def __init__(self):
        super().__init__()
        self.arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)

        self.comms_lock = threading.Lock()

        self.timer = threading.Timer(TIMER_PERIOD, self.get_all_tag_values)
        self.timer.start()

    def get_all_tag_values(self):
        """Periodic function to update tags in this object"""
        with self.comms_lock:
            self.send_message("{}".format(Code.GET_ALL_TAG_VALUES.value))
            tag_values = str(self.get_response()).rstrip('\'')
        splits = tag_values.split(" ")

        # Ignore the response code
        for key, value in pairwise(splits[1:]):
            # Weird thing with b95A lol
            if (key == 'b'):
                key = 'b95A'

            self.tags.update({key : bool(int(value))})

        signals.swtrack_update_gui.emit()

        if HWTrackCtrlConnector.run_timer:
            self.timer = threading.Timer(TIMER_PERIOD, self.get_all_tag_values)
            self.timer.start()

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

    def set_tag_value(self, tag_name, value):
        """Sets a tag's value inside the plc

        :param str tag_name: Name of the tag
        :param bool value: Value to set to the tag to
        """
        def communicate():
            """Private function for a thread to communicate with the arduino"""
            with self.comms_lock:
                self.send_message(" ".join(map(str, (Code.SET_TAG_VALUE.value, tag_name, int(value)))))
                logger.info(self.get_response())
                super().set_tag_value(tag_name, value)

        temp_thread = threading.Thread(target=communicate, daemon=True)
        temp_thread.start()

    def run_program(self):
        """Nothing should be done for the hw controller"""
        pass
