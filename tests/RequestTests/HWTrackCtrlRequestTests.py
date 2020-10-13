"""Tests to ensure the server handles requests cleanly."""

import sys

sys.path.insert(1, '../../src/UI')
from server_functions import send_message, RequestCode, ResponseCode

def test_get_hw_track_controller_response_failure(start_server):
    """Ensures server responds with an error if no response exists.

    PRECONDITIONS: No response exists in the queue
    EXECUTION STEPS: send_message(GET_HW_TRACK_CONTROLLER_RESPONSE)
    POSTCONDITIONS: ResponseCode is ERROR

    """
    response_code, data = send_message(RequestCode.GET_HW_TRACK_CONTROLLER_RESPONSE,
                                       ignore_exceptions=())
    assert response_code == ResponseCode.ERROR

def test_get_hw_track_controller_request(start_server):
    response_code, data = send_message(RequestCode.GET_HW_TRACK_CONTROLLER_REQUEST,
                                       ignore_exceptions=())
    assert response_code == ResponseCode.ERROR

def test_ctc_stuff(start_server):
    response_code, data = send_message(RequestCode.CTC_DISPATCH_TRAIN,
                                       data='32 10 03 25 a',
                                       ignore_exceptions=())
    assert response_code == ResponseCode.ERROR

    response_code, data = send_message(RequestCode.GET_COMMAND_SPEED,
                                       ignore_exceptions=())
    assert response_code == ResponseCode.SUCCESS


if __name__ == "__main__":
    raise Exception("Run using pytest")
