"""API for the HW Track Controller Module."""

from argparse import ArgumentParser
import socket
import sys
from time import sleep
import logging
import polling
import serial

logger = logging.getLogger(__name__)

# Communications with controller
SERIAL_PORT = 'COM3'
RATE = 9600
arduino = serial.Serial(SERIAL_PORT, RATE, timeout=5)
sleep(2)

# Communications with server
# HOST = '18.188.207.58'
HOST = '3.23.104.34'
SERVER_PORT = 1234
HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST = b'105'
HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE = b'106'

def get_request():
    """Retrieves a request from the server.

    :return: RequestCode followed by additional data. RequestCode
    of 0 represents there are no requests pending
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, SERVER_PORT))
        sock.sendall(HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST)
        data = sock.recv(1024)

    return data

def send_request_to_controller(request):
    """Forwards the request from the server to the controller.

    :param request: Request retrieved from the server
    """
    sleep(0.2)
    bytes_written = arduino.write(request)
    logger.info("%d bytes written to the controller", bytes_written)

def get_response_from_controller():
    """Gets the response from the controller.

    :return: Response of the controller to the previous request
    :rtype: bytes
    """
    arduino.flushInput()
    response = arduino.readline()
    logger.info("Response from controller %s", response)
    # Remove \r\n from the end of the response
    return response.rstrip(b'\t\r\n ')

def send_reponse_to_server(response):
    """Sends response of the controller back to the server.

    :param response: Response gathered from the controller
    """
    print(response[1:])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, SERVER_PORT))
        sock.sendall(HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE + b' ' + response)
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
