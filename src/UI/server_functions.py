"""Functions for communicating with the server."""

from enum import Enum
import socket
import threading
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
    ERROR = 1 # Used by the system in the case that there was an error parsing the original request
    DEBUG_TO_CTC = 2
    DEBUG_TO_HWTRACKCTRL = 3
    DEBUG_TO_SWTRACKCTRL = 4
    DEBUG_TO_TRACK_MODEL = 5
    DEBUG_TO_TRAIN_MODEL = 6
    DEBUG_TO_HWTRAINCTRL = 7
    DEBUG_TO_SWTRAINCTRL = 8

    CTC_DISPATCH_TRAIN = 32
    CTC_SEND_GUI_GREEN_OCCUPANCIES = 33
    CTC_SEND_GUI_RED_OCCUPANICES =34
    CTC_UPDATE_AUTHORITY = 35
    CTC_UPDATE_SPEED = 36
    CTC_UPDATE_SIGNAL = 37
    CTC_UPDATE_SCHEDULE = 38
    CTC_UPDATE_AUTOMATIC_MODE = 39
    CTC_UPDATE_SWITCH = 40
    CTC_SEND_GUI_THROUGHPUT = 41
    CTC_SEND_GUI_TRAIN_INFO = 42
    CTC_SEND_GUI_SWITCH_POS_GREEN = 43
    CTC_SEND_GUI_SWITCH_POS_RED = 44
    CTC_SEND_GUI_SIGNAL_INFO = 45
    CTC_SEND_TIMER_REQUEST = 46
    CTC_GIVE_TICKET_SALES = 47 # Used by the track model to give the ctc ticket sales
    CTC_TIME_TRIGGERED = 60
    CTC_GET_SIGNALS = 61
    CTC_GET_TRACK_STATUS = 62
    CTC_GET_OCCUPANCIES = 63

    SWTRACK_DISPATCH_TRAIN = 64 # Used by the CTC to signify that a new train has been dispatched
    SWTRACK_UPDATE_AUTHORITY = 65 # Used by the CTC when a train's authority has been updated
    SWTRACK_SET_TRACK_SIGNAL = 66 # Used by the CTC to set a track block's signal color
    SWTRACK_UPDATE_COMMAND_SPEED = 67 # Used by the CTC when a train's command speed is updated
    SWTRACK_SET_TRACK_STATUS = 68 # Used by the CTC when a block is closed/open for maintenance
    SWTRACK_SET_SWITCH_POSITION = 69 # Used by the CTC when a track switch needs flipped
    SWTRACK_SET_TRACK_FAILURE = 70 # Used by the track model to inform the controller that a failure has occured on a block
    SWTRACK_SET_TRACK_OCCUPANCY = 71 # Used by the track model to inform the controller that a train is on a block
    SWTRACK_SET_CROSSING = 72 # Used by the track model to have the controller lower/raise the crossing
    SWTRACK_SET_TRACK_HEATER = 73 # Used by the Track model to turn on/off the track heater

    # The following request codes are used by the sw track controller gui to download a plc program
    # An offset is used to convert them to hw track controller requests. PLEASE DON'T CHANGE THE NUMBERS!!!
    START_DOWNLOAD = 74 # Used by the gui to start a download
    END_DOWNLOAD = 75 # Used by the gui to end a download
    CREATE_TAG = 76 # Used by the gui to create a tag
    CREATE_TASK = 77 # Used by the gui to create a task
    CREATE_ROUTINE = 78 # Used by the gui to create a routine
    CREATE_RUNG = 79 # Used by the gui to create a rung
    CREATE_INSTRUCTION = 80 # Used by the gui to create an instruction
    SET_TAG_VALUE = 81 # Used by the gui to set a tag's value
    GET_TAG_VALUE = 82 # Used by the gui to get a tag's value

    SWTRACK_GUI_GATHER_DATA = 83 # Used by the gui to periodically gather data from the server
    SWTRACK_GUI_SET_SWITCH_POSITION = 84 # Used by the gui to set a switch's position // (trackController, newPosition)

    HWTRACK_START_DOWNLOAD = 96 # Used by the SW Track Ctrl to signify download is starting # (string programName)
    HWTRACK_END_DOWNLOAD = 97 # Used by the SW Track Ctrl to signify download has completed # (void)
    HWTRACK_CREATE_TAG = 98 # Used by the SW Track Ctrl to create a tag in the hardware # (string tagName bool defaultValue)
    HWTRACK_CREATE_TASK = 99 # Used by the SW Track Ctrl to create a task in the hardware # (string taskType (float period | string event) string taskName)
    HWTRACK_CREATE_ROUTINE = 100 # Used by the SW Track Ctrl to create a routine in the hardware # (string routineName)
    HWTRACK_CREATE_RUNG = 101 # Used by the SW Track Ctrl to create a rung in the hardware # ((void | string rungName))
    HWTRACK_CREATE_INSTRUCTION = 102 # Used by the SW Track Ctrl to create an instruction in the hardware # (instructionType argument)
    HWTRACK_SET_TAG_VALUE = 103 # Used by the SW Track Ctrl to set a tag value # (string tagName bool newValue)
    HWTRACK_GET_TAG_VALUE = 104 # Used by the SW Track Ctrl to get a tag value # (string tagName)
    HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST = 105 # Used by the connector script to check if any requests exist for the hardware
    HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE = 106 # Used by the connector script to forward the hardware's response to the server
    HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE = 107 # Used by SW Track Ctrl to get response from the hardware

    TRACK_MODEL_GUI_TRACK_LAYOUT = 129 # Used by the gui to signify that the track layout is starting to be sent
    TRACK_MODEL_GUI_BLOCK = 130 # Used by the gui to signify that a block is being sent
    TRACK_MODEL_GUI_TRACK_LAYOUT_SECTION = 131 # Used by the gui when the track layout is being imported
    TRACK_MODEL_GUI_SET_TRACK_HEATER = 132 # Used by the gui when the track heater is set
    TRACK_MODEL_GUI_SET_FAILURE = 133 # Used by the gui when a track failure is induced
    TRACK_MODEL_GUI_GATHER_DATA = 134 # Used periodically by the gui to update the user interface
    TRACK_MODEL_GUI_EDIT_BLOCK_LENGTH = 135 # Used by the gui to edit block length
    TRACK_MODEL_GIVE_POSITION = 136 # Used by the train model to give the track model the position of a train
    TRACK_MODEL_UPDATE_COMMAND_SPEED = 137 # Used by the track controller to update the command speed of a train
    TRACK_MODEL_UPDATE_SWITCH_POSITIONS = 138 # Used by the track controller to update a switch positions
    TRACK_MODEL_UPDATE_AUTHORITY = 139 # Used by the track controller to update the authority of a train
    TRACK_MODEL_DISPATCH_TRAIN = 140 # Used by the track controller to signify that a new train has been dispatched

    TRAIN_MODEL_GUI_GATHER_DATA = 160 # Used periodically by the gui to update the user interface
    TRAIN_MODEL_DISPATCH_TRAIN = 161 # Used by the track model to signify that a new train has been dispatched
    TRAIN_MODEL_UPDATE_AUTHORITY = 162 # Used by the track model to update a train's authority
    TRAIN_MODEL_UPDATE_COMMAND_SPEED = 163 # Used by the track model to update a train's command speed
    TRAIN_MODEL_SET_THE_DAMN_LIGHTS = 164 # Used by the track model to let the train model know that the train is in a tunnel
    TRAIN_MODEL_GIVE_POWER = 165 # Used by the train controller to give the train model a value for power
    TRAIN_MODEL_GUI_CAUSE_FAILURE = 166 # Used by the gui to cause a train failure
    TRAIN_MODEL_GUI_SET_TRAIN_LENGTH = 167 # Used by the gui to set a train's length
    TRAIN_MODEL_GUI_SET_TRAIN_MASS = 168 # Used by the gui to set a train's mass
    TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT = 169 # Used by the gui to set a train's height
    TRAIN_MODEL_GUI_SET_TRAIN_WIDTH = 170 # Used by the gui to set a train's width
    TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT = 171 # Used by the gui to set a train's passenger count
    TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT = 172 # Used by the gui to set a train's crew count

    SWTRAIN_DISPATCH_TRAIN = 192 # Used by the train model to signify that a new train has been dispatched
    SWTRAIN_UPDATE_CURRENT_SPEED = 193 # Used by the train model to update a train's current speed
    SWTRAIN_UPDATE_COMMAND_SPEED = 194 # Used by the train model to update a train's command speed
    SWTRAIN_UPDATE_SPEED_LIMIT = 195 # Used by the train model to update a train's speed limit
    SWTRAIN_UPDATE_AUTHORITY = 196 # Used by the train model to update a train's authority
    SWTRAIN_CAUSE_FAILURE = 197 # Used by the train model to cause a train's failure
    SWTRAIN_PULL_PASSENGER_EBRAKE = 198 # Used by the train model to pull a train's passenger e-brake
    SWTRAIN_GUI_GATHER_DATA = 199 # Used by the gui to update the user interface
    SWTRAIN_GUI_PULL_EBRAKE = 200 # Used by the gui to pull the train's ebrake
    SWTRAIN_GUI_SET_SETPOINT_SPEED = 201 # Used by the gui to set a train's setpoint speed
    SWTRAIN_GUI_PRESS_SERVICE_BRAKE = 202 # Used by the gui to update use a train's service brake
    SWTRAIN_GUI_TOGGLE_DAMN_DOORS = 203 # Used by the gui to toggle a train's door
    SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS = 204 # Used by the gui to toggle a train's lights
    SWTRAIN_GUI_SET_SEAN_PAUL = 205 # Used by the gui to play temperature by sean paul
    SWTRAIN_GUI_ANNOUNCE_STATIONS = 206 # Used by the gui to announce stations
    SWTRAIN_GUI_DISPLAY_ADS = 207 # Used by the gui to display a train's advertisements
    SWTRAIN_GUI_RESOLVE_FAILURE = 208 # Used by the gui to resolve a train failure
    SWTRAIN_GUI_SET_KP_KI = 209 # Used by the gui to set a train's kp/ki
    SWTRAIN_GUI_SWITCH_MODE = 210 # Used by gui to switch between automatic and manual mode
    SWTRAIN_TIME_TRIGGER = 211 # Used to trigger PID loop and calculate power

    HWTRAIN_PULL_EBRAKE = 224 # Used by the SW Train Ctrl to pull the train's ebrake
    HWTRAIN_SET_SETPOINT_SPEED = 225 # Used by the SW Train Ctrl to set a train's setpoint speed
    HWTRAIN_PRESS_SERVICE_BRAKE = 226 # Used by the SW Train Ctrl to update use a train's service brake
    HWTRAIN_TOGGLE_DAMN_DOORS = 227 # Used by the SW Train Ctrl to toggle a train's door
    HWTRAIN_TOGGLE_CABIN_LIGHTS = 228 # Used by the SW Train Ctrl to toggle a train's lights
    HWTRAIN_SET_TEMPERATURE = 229 # Used by the SW Train Ctrl to play temperature by sean paul
    HWTRAIN_ANNOUNCE_STATIONS = 230 # Used by the SW Train Ctrl to announce stations
    HWTRAIN_DISPLAY_ADS = 231 # Used by the SW Train Ctrl to display a train's advertisements
    HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST = 232 # Used by the connector script to check if any requests exist for the hardware
    HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE = 233 # Used by the connector script to forward the hardware's response to the server
    HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE = 234 # Used by SW Train Ctrl to get response from the hardware
    HWTRAIN_DISPATCH_TRAIN = 235 # Used by SWTrainController to signify a train has been dispatched


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

    HWTRACK_SET_TAG_VALUE = 103
    HWTRACK_GET_TAG_VALUE = 104

def send_message(request_code, data="", ignore_exceptions=(ConnectionRefusedError)):
    """Constructs and sends a message to the server

    :param RequestCode request_code: Code representing what the request is for
    :param str data: String containing additional data

    :return: Response code and accompanying data
    :rtype: tuple

    """
    request = bytes(str(request_code.value), 'utf-8') + b' ' + bytes(data, 'utf-8')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(request)
            data = sock.recv(1024)
    except ignore_exceptions:
        # Show up as an error
        data = b'1'

    # Remove byte stuff and split along first space
    splits = repr(data)[2:-1].split(" ", 1)
    try:
        response_code = int(splits[0])
    except ValueError:
        response_code = ResponseCode.ERROR

    # If there's additional response data, capture it
    if len(splits) > 1:
        response_data = str(splits[1])
    else:
        response_data = ""

    return (ResponseCode(response_code), response_data)

def send_message_async(request_code, data, callback,
                       ignore_exceptions=(ConnectionRefusedError)):
    """Sends a given message to a server asynchronously

    :param RequestCode request_code: Code representing what the request is for
    :param str data: String containing additional data
    :param Callable callback: Function to be called after the response is received
    :param set ignore_exceptions: Exceptions to be ignored

    """
    thread = threading.Thread(target=_send_message_async,
                              args=(request_code, data, callback, ignore_exceptions),
                              daemon=True)
    thread.start()

def _send_message_async(request_code, data, callback,
                        ignore_exceptions=(ConnectionRefusedError)):
    """Internal function used as helper to send_message_async"""
    # Send the message
    response_code, response_data = send_message(request_code, data, ignore_exceptions)

    # Invoke the callback
    callback(response_code, response_data)

def poll_for_response(request_code, data="", expected_response=ResponseCode.SUCCESS,
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
                                step=0.75,
                                timeout=timeout,
                                check_success=lambda x: x[0] == expected_response)
    except polling.TimeoutException:
        response = (ResponseCode.ERROR, "")
        logger.error("Timeout occurred")
    return response


if __name__ == "__main__":
    raise Exception("Not to be run as a module")
