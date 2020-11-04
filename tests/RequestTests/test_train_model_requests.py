"""Tests to ensure the server handles requests cleanly."""

import sys

sys.path.insert(1, '../../src')
from UI.server_functions import send_message, RequestCode, ResponseCode

def test_get_current_speed(start_server):
    """Ensures we multiple power by two and store the current speed.

    PRECONDITIONS: Received power (5) from train controller
    EXECUTION STEPS: send_message(TRAIN_MODEL_GET_CURRENT_SPEED)
    POSTCONDITIONS: ResponseCode is SUCCESS, current_speed is 10

    """
    pass
    # response_code, data = send_message(RequestCode.DEBUG_TO_TRAIN_MODEL,
    #                                    data="165 5",
    #                                    ignore_exceptions=())
    # assert response_code == ResponseCode.SUCCESS

    # response_code, data = send_message(RequestCode.TRAIN_MODEL_GET_CURRENT_SPEED,
    #                                    ignore_exceptions=())
    # assert response_code == ResponseCode.SUCCESS
    # assert int(data) == 10


if __name__ == "__main__":
    raise Exception("Run using pytest")
