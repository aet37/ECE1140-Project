"""Module defining signals for communications"""

from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    lights_toggled = pyqtSignal(bool)

    # CTC Signals
    update_green_occupancies = pyqtSignal(list)	# Used by SWTrack Controller to send CTC green line occupancies in array of BOOL
    update_red_occupancies = pyqtSignal(list)	# Used by SWTrack Controller to send CTC red line occupancies in array of BOOL
    update_green_switches = pyqtSignal(list)	# Used by SWTrack Controller to send CTC green line switches in array of BOOL
    update_red_switches = pyqtSignal(list)		# Used by SWTrack Controller to send CTC red line switches in array of BOOL
    update_throughput = pyqtSignal(int)			# Used by Track Model to send CTC throughput (ticket sales)


    # Track Controller Signals
    swtrack_dispatch_train = pyqtSignal(int, int, int, int, Line, list) # Used by CTC to send dispatch Train (train_id, destination_block, command_speed, authority, Line, switches_arr(boolean))
    swtrack_update_authority = pyqtSignal(int, int)	# Used by CTC to update authority of a train (train_id, new_authority)
    swtrack_update_speed = pyqtSignal(int, int)	# Used by CTC to update suggested speed of train (train_id, new_speed)
    swtrack_set_switch_position = pyqtSignal(int, bool)	# Used by CTC to set a switch position in maint mode (sw_number, position)
    swtrack_set_block_status = pyqtSignal(int, bool)	# Used by CTC to open/close (true/false) a block for mainenence (block_num, status)

    # SWTrainController Signals
    # SWTrainController Signals #
    SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS = pyqtSignal(int) # TrainID
    SWTRAIN_DISPATCH_TRAIN = pyqtSignal(float, float, bool) # command speed, current speed, authority
    SWTRAIN_UPDATE_CURRENT_SPEED = pyqtSignal(int, float) # TrainID, current speed
    SWTRAIN_UPDATE_COMMAND_SPEED = pyqtSignal(int, float) # TrainID, command speed 
    SWTRAIN_UPDATE_AUTHORITY = pyqtSignal(int, bool) # TrainID, authority
    SWTRAIN_CAUSE_FAILURE = pyqtSignal(bool, bool, bool) # Failures
    SWTRAIN_PULL_PASSENGER_EBRAKE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_PULL_EBRAKE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_SET_SETPOINT_SPEED = pyqtSignal(int, float) # TrainID, Setpoint Speed
    SWTRAIN_GUI_PRESS_SERVICE_BRAKE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_TOGGLE_DAMN_DOORS = pyqtSignal(int) # TrainID 
    SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_SET_SEAN_PAUL = pyqtSignal(int, float) # TrainID, temperature
    SWTRAIN_GUI_ANNOUNCE_STATIONS = pyqtSignal(int) # TrainID 
    SWTRAIN_GUI_DISPLAY_ADS = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_RESOLVE_FAILURE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_SET_KP_KI = pyqtSignal(int, float, float) # TrainID, setKp, setKi
    SWTRAIN_GUI_SWITCH_MODE = pyqtSignal(int, str) # TrainID, override code
    SWTRAIN_TIME_TRIGGER = pyqtSignal()

# Single instance to be used by other modules
signals = SignalsClass()
