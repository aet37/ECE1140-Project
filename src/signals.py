"""Module defining signals for communications"""

from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    timer_expired = pyqtSignal(int, int, int) # Current hours, minutes, seconds
    lights_toggled = pyqtSignal(bool)

    # CTC Signals
    update_green_occupancies = pyqtSignal(list)	# Used by SWTrack Controller to send CTC green line occupancies in array of BOOL
    update_red_occupancies = pyqtSignal(list)	# Used by SWTrack Controller to send CTC red line occupancies in array of BOOL
    update_green_switches = pyqtSignal(list)	# Used by SWTrack Controller to send CTC green line switches in array of BOOL
    update_red_switches = pyqtSignal(list)		# Used by SWTrack Controller to send CTC red line switches in array of BOOL
    update_throughput = pyqtSignal(int)			# Used by Track Model to send CTC throughput (ticket sales)
    dispatch_scheduled_train = pyqtSignal(int, Line)	# Used by Timekeeper to send CTC a dispatch commmand


    # Track Controller Signals
    swtrack_dispatch_train = pyqtSignal(int, int, int, int, Line, list) # Used by CTC to send dispatch Train (train_id, destination_block, command_speed, authority, Line, switches_arr(BOOL))
    swtrack_update_authority = pyqtSignal(int, int)	# Used by CTC to update authority of a train (train_id, new_authority)
    swtrack_update_speed = pyqtSignal(int, int)	# Used by CTC to update suggested speed of train (train_id, new_speed)
    swtrack_set_switch_position = pyqtSignal(int, bool)	# Used by CTC to set a switch position in maint mode (sw_number, position)
    swtrack_set_block_status = pyqtSignal(int, bool)	# Used by CTC to open/close (true/false) a block for mainenence (block_num, status)

# Single instance to be used by other modules
signals = SignalsClass()
