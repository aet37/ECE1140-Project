"""Tests to ensure the server handles requests cleanly."""

import sys

sys.path.insert(1, '../../src/UI')
from server_functions import send_message, RequestCode, ResponseCode

def test_get_hw_track_controller_request_no_requests(start_server):
    """Ensures server responds with an error if no request exists

    PRECONDITIONS: No request exists in the queue
    EXECUTION STEPS: send_message(HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST)
    POSTCONDITIONS: ResponseCode is ERROR

    """
    response_code, data = send_message(RequestCode.HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST,
                                       ignore_exceptions=())
    assert response_code == ResponseCode.ERROR

def test_get_hw_track_controller_request(start_server):
    """Ensures server responds with an expected request on the queue

    PRECONDITIONS: A request containing (HWTRACK_SET_TAG_VALUE, "Switch1 1") is on the request queue
    EXECUTION STEPS: send_message(HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST)
    POSTCONDITIONS: ResponseCode is HWTRACK_SET_TAG_VALUE, and data is 1

    """
    response_code, data = send_message(RequestCode.HWTRACK_SET_TAG_VALUE,
                                       data="Switch1 1",
                                       ignore_exceptions=())
    assert response_code == ResponseCode.SUCCESS

    response_code, data = send_message(RequestCode.HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST,
                                       ignore_exceptions=())
    assert response_code == ResponseCode.HWTRACK_SET_TAG_VALUE
    assert "Switch1 1" == data

def test_get_hw_track_controller_response(start_server):
    """Ensures server responds with an expected response

    PRECONDITIONS: A response containing (SUCCESS, "1") is on the response queue
    EXECUTION STEPS: send_message(HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE)
    POSTCONDITIONS: ResponseCode is SUCCESS, data is "1"

    """
    response_code, data = send_message(RequestCode.HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE,
                                       data="1",
                                       ignore_exceptions=())
    assert ResponseCode.SUCCESS == response_code

    response_code, data = send_message(RequestCode.HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE,
                                       ignore_exceptions=())
    assert ResponseCode.SUCCESS == response_code
    assert "1" == data

def test_get_hw_track_controller_response_failure(start_server):
    """Ensures server responds with an error if no response exists.

    PRECONDITIONS: No response exists in the queue
    EXECUTION STEPS: send_message(HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE)
    POSTCONDITIONS: ResponseCode is ERROR

    """
    response_code, data = send_message(RequestCode.HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE,
                                       ignore_exceptions=())
    assert response_code == ResponseCode.ERROR


if __name__ == "__main__":
    raise Exception("Run using pytest")
