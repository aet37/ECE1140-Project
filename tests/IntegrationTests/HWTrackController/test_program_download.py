"""Test for downloading a program to the arduino"""

import sys
from time import sleep

sys.path.insert(1, '../../../src')
from HWTrackController.hw_track_controller_connector import send_request_to_controller, \
                                                            get_response_from_controller
from UI.server_functions import RequestCode

def test_blank_controller():
    """Ensure we can start then immediately end a download"""
    # Start download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_START_DOWNLOAD.value), 'utf-8') +
                                     bytes(" Blank Program", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # End download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_END_DOWNLOAD.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

def test_program_download():
    """Downloads a simple program to the arduino"""
    # Start download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_START_DOWNLOAD.value), 'utf-8') +
                                     bytes(" LED Toggle Program", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a tag
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_TAG.value), 'utf-8') +
                                     bytes(" MyTag", 'utf-8') +
                                     bytes(" FALSE", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_TAG.value), 'utf-8') +
                                     bytes(" output2", 'utf-8') +
                                     bytes(" FALSE", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a periodic task
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_TASK.value), 'utf-8') +
                                     bytes(" PERIOD 2000 MainTask", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create the main routine
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_ROUTINE.value), 'utf-8') +
                                     bytes(" Main", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add three instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIC MyTag", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIC output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" OTU output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a new rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add three instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIO MyTag", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIO output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" OTL output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a new rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add two instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIO output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" OTU MyTag", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a new rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add two instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIC output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" OTL MyTag", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # End download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_END_DOWNLOAD.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

def test_lcd_downloading():
    """Verify that the lcd display shows Downloading... during a download"""
    # Start download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_START_DOWNLOAD.value), 'utf-8') +
                                     bytes(" Test Program", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Given some time for verification
    sleep(10)

    # End download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_END_DOWNLOAD.value), 'utf-8'))
    assert get_response_from_controller() == b'0'


if __name__ == "__main__":
    raise Exception("Run using pytest")
