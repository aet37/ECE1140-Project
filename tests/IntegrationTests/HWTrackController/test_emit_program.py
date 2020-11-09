"""Test for downloading a program to the arduino"""

import sys
from time import sleep

sys.path.insert(1, '../../../src')
from HWTrackController.hw_track_controller_connector import send_request_to_controller, \
                                                            get_response_from_controller
from UI.server_functions import RequestCode

def test_emit_program():
    """Downloads a program that uses an EMIT instruction"""
    # Start download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_START_DOWNLOAD.value), 'utf-8') +
                                     bytes(" Emit Program", 'utf-8'))
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
                                     bytes(" PERIOD 1000 MainTask", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create the main routine
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_ROUTINE.value), 'utf-8') +
                                     bytes(" Main", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" XIC MyTag", 'utf-8'))
    assert get_response_from_controller() == b'0'

    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" EMIT MyTagEvent", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create an event driven task
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_TASK.value), 'utf-8') +
                                     bytes(" EVENT MyTagEvent EventDrivenTask", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create the main routine
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_ROUTINE.value), 'utf-8') +
                                     bytes(" Main", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Create a rung
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_RUNG.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Add instructions
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_CREATE_INSTRUCTION.value), 'utf-8') +
                                     bytes(" OTL output2", 'utf-8'))
    assert get_response_from_controller() == b'0'

    # End download
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_END_DOWNLOAD.value), 'utf-8'))
    assert get_response_from_controller() == b'0'

    # Wait a few seconds before setting the tag
    sleep(5)

    # Set MyTag
    send_request_to_controller(bytes(str(RequestCode.HWTRACK_SET_TAG_VALUE.value), 'utf-8') +
                                     bytes(" MyTag 1", 'utf-8'))
    assert get_response_from_controller() == b'0'


if __name__ == "__main__":
    raise Exception("Run using pytest")
