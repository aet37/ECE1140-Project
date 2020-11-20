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
    swtrain_gui_toggle_cabin_lights = pyqtSignal(int) # TrainID
    swtrain_dispatch_train = pyqtSignal(float, float, bool) # command speed, current speed, authority
    swtrain_update_current_speed = pyqtSignal(int, float) # TrainID, current speed
    swtrain_update_command_speed = pyqtSignal(int, float) # TrainID, command speed 
    swtrain_update_authority = pyqtSignal(int, bool) # TrainID, authority
    swtrain_cause_failure = pyqtSignal(bool, bool, bool) # Failures
    swtrain_pull_passenger_ebrake = pyqtSignal(int) # TrainID
    swtrain_gui_pull_ebrake = pyqtSignal(int) # TrainID
    swtrain_gui_set_setpoint_speed = pyqtSignal(int, float) # TrainID, Setpoint Speed
    swtrain_gui_press_service_brake = pyqtSignal(int) # TrainID
    swtrain_gui_toggle_damn_doors = pyqtSignal(int) # TrainID 
    swtrain_gui_toggle_cabin_lights = pyqtSignal(int) # TrainID
    swtrain_gui_set_sean_paul = pyqtSignal(int, float) # TrainID, temperature
    swtrain_gui_announce_stations = pyqtSignal(int) # TrainID 
    swtrain_gui_display_ads = pyqtSignal(int) # TrainID
    swtrain_gui_resolve_failure = pyqtSignal(int) # TrainID
    swtrain_gui_set_kp_ki = pyqtSignal(int, float, float) # TrainID, setKp, setKi
    swtrain_gui_switch_mode = pyqtSignal(int, str) # TrainID, override code
    swtrain_time_trigger = pyqtSignal()

# Single instance to be used by other modules
signals = SignalsClass()
