"""Functions for communicating with the server."""

from enum import Enum
import socket
import logging
import polling

logger = logging.getLogger(__name__)

HOST = '3.23.104.34'  # The server's hostname or IP address
PORT = 1234        # The port used by the server

class RequestCode(Enum):
    """Codes to begin communication to the server

    System wide: 0 - 31
    CTC: 32 - 63
    Software Track Controller: 64 - 95
    Hardware Track Controller: 96 - 127
    Track Model: 128 - 159
    Train Model: 160 - 191
    Software Train Controller: 192 - 223
    Hardware Train Controller: 224 - 255
    """
    ERROR = 1
    LOGIN = 2

    CTC_DISPATCH_TRAIN = 32

    SET_SWITCH_POSITION = 96
    GET_SWITCH_POSITION = 97
    GET_HW_TRACK_CONTROLLER_REQUEST = 100
    SEND_HW_TRACK_CONTROLLER_RESPONSE = 101

    GET_COMMAND_SPEED = 160

class ResponseCode(Enum):
    """Codes to begin communication from the server

    System wide: 0 - 31
    CTC: 32 - 63
    Software Track Controller: 64 - 95
    Hardware Track Controller: 96 - 127
    Track Model: 128 - 159
    Train Model: 160 - 191
    Software Train Controller: 192 - 223
    Hardware Train Controller: 224 - 255
    """
    SUCCESS = 0
    ERROR = 1

def send_message(request_code, data=""):
    """Constructs and sends a message to the server

    :param RequestCode request_code: Code representing what the request is for
    :param str data: String containing additional data

    :return: Response code and accompanying data
    :rtype: tuple

    """
    request = bytes(str(request_code.value), 'utf-8') + b' ' + bytes(data, 'utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(request)
        data = sock.recv(1024)

    # Remove byte stuff and split along first space
    splits = repr(data)[2:-1].split(" ", 1)
    response_code = int(splits[0])

    # If there's additional response data, capture it
    if len(splits) > 1:
        response_data = str(splits[1])
    else:
        response_data = ""

    return (ResponseCode(response_code), response_data)

def poll_for_response(request_code, data, expected_response=ResponseCode.SUCCESS,
                      timeout=5):
    """Continually sends a message until expected_response is received.

    :param RequestCode request_code: Code representing what the request is for
    :param str data: String containing additional data
    :param ResponseCode expected_response: Response from server to expect
    :param float timeout: How long to wait for

    :return: Response code and accompanying data. ResponseCode.ERROR will be returned
    in the event of a timeout
    :rtype: tuple

    """
    try:
        response = polling.poll(send_message,
                                args=[request_code, data],
                                step=0.25,
                                timeout=timeout,
                                check_success=lambda x: x[0] == expected_response)
    except polling.TimeoutException:
        response = (ResponseCode.ERROR, "")
        logger.error("Timeout occurred")
    return response


if __name__ == "__main__":
    raise Exception("Not to be run as a module")
