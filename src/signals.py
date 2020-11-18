"""Module defining signals for communications"""

from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

from common_def import *

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

    # Train Model Signals
    TRAIN_MODEL_DISPATCH_TRAIN = pyqtSignal(int, int, float, int, int) #  Used by the track model to signify that a new train has been dispatched FORMAT: (train_id, destination_block, command_speed, authority, Line)
    TRAIN_MODEL_RECEIVE_BLOCK = pyqtSignal(int, int, float, float, float, float, int) #  Used by the track model to send a block's information FORMAT: (track_id, block_id, elevation, slope, sizeOfBlock, speedLimit, travelDirection)
    # TRAIN_MODEL_GUI_1_GATHER_DATA = 161 #  Used periodically by the gui to update page 1 the user interface
    # TRAIN_MODEL_GUI_2_GATHER_DATA = 162 #  Used periodically by the gui to update page 2 the user interface
    # TRAIN_MODEL_GUI_3_GATHER_DATA = 163 #  Used periodically by the gui to update page 3 the user interface
    TRAIN_MODEL_GUI_SET_TRAIN_LENGTH = pyqtSignal(int, int) #  Used by the gui to set a train's length FORMAT: (train_id, train_length)
    TRAIN_MODEL_GUI_SET_TRAIN_MASS = pyqtSignal(int, int) #  Used by the gui to set a train's mass FORMAT: (train_id, train_mass)
    TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT = pyqtSignal(int, int) #  Used by the gui to set a train's height FORMAT: (train_id, train_height)
    TRAIN_MODEL_GUI_SET_TRAIN_WIDTH = pyqtSignal(int, int) #  Used by the gui to set a train's width FORMAT: (train_id, train_width)
    TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT = pyqtSignal(int, int) #  Used by the gui to set a train's passenger count FORMAT: (train_id, train_pass_count)
    TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT = pyqtSignal(int, int) #  Used by the gui to set a train's crew count FORMAT: (train_id, train_crew_count)
    # TRAIN_MODEL_GUI_UPDATE_DROP_DOWN = 170 #  Used by the gui to update the drop-down that contains the trains
    TRAIN_MODEL_GUI_RECEIVE_LIGHTS = pyqtSignal(int, bool) #  Used by the swtrain to toggle lights FORMAT: (train_id, light_status)
    TRAIN_MODEL_GUI_RECEIVE_EBRAKE = pyqtSignal(int, bool) #  Used by the gui to pull the train's ebrake FORMAT: (train_id, ebrake_status)
    TRAIN_MODEL_GUI_RECEIVE_SERVICE_BRAKE = pyqtSignal(int, bool) #  Used by the gui to update use a train's service brake FORMAT: (train_id, sbrake_status)
    TRAIN_MODEL_GUI_RECEIVE_DOORS = pyqtSignal(int, bool) #  Used by the gui to toggle a train's door FORMAT: (train_id, doors_status)
    TRAIN_MODEL_GUI_RECEIVE_SEAN_PAUL = pyqtSignal(int, float) #  Used by the gui to play temperature by sean paul FORMAT: (train_id, temp_status)
    TRAIN_MODEL_GUI_RECEIVE_ANNOUNCE_STATIONS = pyqtSignal(int, bool) #  Used by the gui to announce stations FORMAT: (train_id, announcements_status)
    TRAIN_MODEL_GUI_RECEIVE_ADS = pyqtSignal(int, bool) #  Used by the gui to display a train's advertisements FORMAT: (train_id, advertisements_status)
    # TRAIN_MODEL_GUI_RECEIVE_RESOLVE_FAILURE = 178 #  Used by the gui to resolve a train failure
    TRAIN_MODEL_RECEIVE_POWER = pyqtSignal(int, float) #  Used by the sw train controller to set a train's kp/ki FORMAT: (train_id, power_update)
    TRAIN_MODEL_GUI_RECEIVE_MODE = pyqtSignal(int, bool) #  Used by gui to switch between automatic and manual mode FORMAT: (train_id, mode_status)

# Single instance to be used by other modules
signals = SignalsClass()
