"""API for the HW Track Controller Module."""

from argparse import ArgumentParser
import socket
import sys
import logging
import polling
import serial

logger = logging.getLogger(__name__)

# Communications with controller
SERIAL_PORT = 'COM6'
RATE = 9600
arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)

# Communications with server
HOST = '3.23.104.34'
SERVER_PORT = 1234
HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST = b'232'
HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE = b'233'

def get_request():
    """Retrieves a request from the server.

    :return: RequestCode followed by additional data. RequestCode
    of 0 represents there are no requests pending
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, SERVER_PORT))
        sock.sendall(HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST)
        data = sock.recv(1024)

    return data

def send_request_to_controller(request):
    """Forwards the request from the server to the controller.

    :param request: Request retrieved from the server
    """
    bytes_written = arduino.write(request)
    logger.info("%d bytes written to the controller", bytes_written)

def get_response_from_controller():
    """Gets the response from the controller.

    :return: Response of the controller to the previous request
    :rtype: bytes
    """
    arduino.flushInput()
    response = arduino.readline()
    logger.info("Response from controller %s", response[:-2])
    # Remove \r\n from the end of the response
    return response[:-2]

def send_reponse_to_server(response):
    """Sends response of the controller back to the server.

    :param response: Response gathered from the controller
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, SERVER_PORT))
        sock.sendall(HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE + response[1:])
        data = sock.recv(1024)

    logger.info("Received %s from server", data)

    if data != b'0':
        logger.error("Error response from server")

def main():
    """Main entry point for the script."""
    argument_parser = ArgumentParser(
        prog='python hw_track_controller_api.py',
        description='Polls the server to check for request from '
                    'the hw track controller. Fulfills requests if any are found'
	)
    argument_parser.add_argument('--verbose', '-v', action='store_true')
    args = argument_parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Continually check and fulfill requests
    while True:
        request = polling.poll(get_request,
                               step=1,
                               poll_forever=True,
                               ignore_exceptions=ConnectionRefusedError,
                               check_success=lambda x: x != b'1')
        logger.info("Request found : %s", request)

        # Forward the request to the controller
        send_request_to_controller(request)

        # Gather the response bytes from the controller
        response = get_response_from_controller()

        # Forward response back to the server
        send_reponse_to_server(response)


if __name__ == "__main__":
    sys.exit(main())
