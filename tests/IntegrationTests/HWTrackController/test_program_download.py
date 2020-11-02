"""Test for downloading a program to the arduino"""

import serial
import sys
import pytest
from time import sleep

sys.path.insert(1, '../../../src')
from HWTrackController.hw_track_controller_connector import *
from UI.server_functions import RequestCode, ResponseCode

def test_program_download():
    """Downloads a program to the arduino"""

    # Start download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_START_DOWNLOAD.value), 'utf-8') +
                                     bytes(" Test Program", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a tag
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_TAG.value), 'utf-8') +
                                     bytes(" myTag", 'utf-8') +
                                     bytes(" FALSE", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a periodic task
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_TASK.value), 'utf-8') +
                                     bytes(" PERIOD", 'utf-8') +
                                     bytes(' 1000', 'utf-8') +
                                     bytes(" MainTask", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create the main routine
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_ROUTINE.value), 'utf-8') +
                                     bytes(" Main", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add two instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIC myTag", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # End download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_END_DOWNLOAD.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

if __name__ == "__main__":
    raise Exception("Run using pytest")