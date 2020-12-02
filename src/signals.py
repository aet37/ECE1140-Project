"""Module defining signals for communications"""

from typing import List
from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    timer_expired = pyqtSignal(int, int, int, int) # Current day, hours, minutes, seconds

    # CTC Signals
    update_occupancy = pyqtSignal(Line, int, bool)	# Used by SWTrack Controller to send CTC updated occupanices
    update_green_switches = pyqtSignal(list)	# Used by SWTrack Controller to send CTC green line switches in array of BOOL
    update_red_switches = pyqtSignal(list)		# Used by SWTrack Controller to send CTC red line switches in array of BOOL
    update_throughput = pyqtSignal(int)			# Used by Track Model to send CTC throughput (ticket sales)
    dispatch_scheduled_train = pyqtSignal(int, Line)	# Used by Timekeeper to send CTC a dispatch commmand
    update_failure_blocks = pyqtSignal(Line, int, bool) # Used by the swtrack to send blocks that are being closed for maintenance or finished with maintenance (line, blockNumber, failureBool)
    ctc_update_failure_blocks_gui = pyqtSignal(Line, bool) # Update the GUI to dispaly closed blocks correctly

    # Track Controller Signals
    swtrack_dispatch_train = pyqtSignal(int, int, int, int, Line, list) # Used by CTC to send dispatch Train (train_id, destination_block, command_speed, authority, Line, switches_arr(BOOL))
    swtrack_update_authority = pyqtSignal(int, int)	# Used by CTC to update authority of a train (train_id, new_authority)
    swtrack_update_speed = pyqtSignal(int, int)	# Used by CTC to update suggested speed of train (train_id, new_speed)
    swtrack_set_switch_position = pyqtSignal(Line, int, bool)	# Used by CTC to set a switch position in maint mode (sw_number, position)
    swtrack_set_block_status = pyqtSignal(Line, int, bool, int)	# Used by CTC to open/close (true/false) a block for mainenence (block_num, status)
    swtrack_force_authority_reevaluation = pyqtSignal(Line) # Used by anyone to force all authorities on a line to be reevaluated

    swtrack_update_occupancies = pyqtSignal(int, Line, int, bool) # Used by Track Model to update occupancies (trainId, Line, blockNumber, occupancy) occupancy = 0  for empty, 1 for occupied
    swtrack_set_track_heater = pyqtSignal(Line, bool) # Used by the Track Model to turn the heater on/off on a track
    swtrack_update_gui = pyqtSignal() # Used by the swtrack to let that gui know that it needs to update
    swtrack_update_broken_rail_failure = pyqtSignal(Line, int, bool) # Used by the Track Model to notify swtrack controller of a broken rail failure
    swtrack_update_power_failure = pyqtSignal(Line, int, bool) # Used by the Track Model to notify swtrack controller of a power failure
    swtrack_update_track_circuit_failure = pyqtSignal(Line, int, bool) # Used by the Track Model to notify swtrack controller of a track circuit failure


    # Train Model Signals
    train_model_dispatch_train = pyqtSignal(int, int, float, int, Line, list) #  Used by the track model to signify that a new train has been dispatched FORMAT: (train_id, destination_block, command_speed, authority, Line, route)
    train_model_receive_block = pyqtSignal(int, int, float, float, float, float, int, bool, Beacon, Beacon) #  Used by the track model to send a block's information FORMAT: (track_id, block_id, elevation, slope, sizeOfBlock, speedLimit, travelDirection, station, newBeacon1, newBeacon2)
    # train_model_gui_1_gather_data = 161 #  Used periodically by the gui to update page 1 the user interface
    # train_model_gui_2_gather_data = 162 #  Used periodically by the gui to update page 2 the user interface
    # train_model_gui_3_gather_data = 163 #  Used periodically by the gui to update page 3 the user interface
    train_model_gui_set_train_length = pyqtSignal(int, int) #  Used by the gui to set a train's length FORMAT: (train_id, train_length)
    train_model_gui_set_train_mass = pyqtSignal(int, int) #  Used by the gui to set a train's mass FORMAT: (train_id, train_mass)
    train_model_gui_set_train_height = pyqtSignal(int, int) #  Used by the gui to set a train's height FORMAT: (train_id, train_height)
    train_model_gui_set_train_width = pyqtSignal(int, int) #  Used by the gui to set a train's width FORMAT: (train_id, train_width)
    train_model_gui_set_train_passenger_count = pyqtSignal(int, int) #  Used by the gui to set a train's passenger count FORMAT: (train_id, train_pass_count)
    train_model_gui_set_train_crew_count = pyqtSignal(int, int) #  Used by the gui to set a train's crew count FORMAT: (train_id, train_crew_count)
    train_model_gui_update_drop_down = pyqtSignal(int) #  Used by the gui to update the drop-down that contains the trains
    train_model_gui_receive_lights = pyqtSignal(int, bool) #  Used by the swtrain to toggle lights FORMAT: (train_id, light_status)
    train_model_gui_receive_ebrake = pyqtSignal(int, bool) #  Used by the gui to pull the train's ebrake FORMAT: (train_id, ebrake_status)
    train_model_gui_receive_service_brake = pyqtSignal(int, bool) #  Used by the gui to update use a train's service brake FORMAT: (train_id, sbrake_status)
    train_model_gui_receive_doors = pyqtSignal(int, bool) #  Used by the gui to toggle a train's door FORMAT: (train_id, doors_status)
    train_model_gui_receive_sean_paul = pyqtSignal(int, float) #  Used by the gui to play temperature by sean paul FORMAT: (train_id, temp_status)
    train_model_gui_receive_announce_stations = pyqtSignal(int, bool) #  Used by the gui to announce stations FORMAT: (train_id, announcements_status)
    train_model_gui_receive_ads = pyqtSignal(int, bool) #  Used by the gui to display a train's advertisements FORMAT: (train_id, advertisements_status)
    # train_model_gui_receive_resolve_failure = 178 #  Used by the gui to resolve a train failure
    train_model_receive_power = pyqtSignal(int, float) #  Used by the sw train controller to set a train's kp/ki FORMAT: (train_id, power_update)
    train_model_gui_receive_mode = pyqtSignal(int, bool) #  Used by gui to switch between automatic and manual mode FORMAT: (train_id, mode_status)
    train_model_something_has_been_changed = pyqtSignal() #  Used by gui to know that something has been changed FORMAT: ()
    train_model_dropdown_has_been_changed = pyqtSignal() #  Used by gui to know that something has been changed FORMAT: ()
    train_model_update_command_speed = pyqtSignal(int, float) # Used by the track model to update the command speed of a train (trainId, newSpeed)
    train_model_update_authority = pyqtSignal(int, bool) # Used by the Track Model to update the authority of a train (trainId, newAuthority)
    train_model_update_passengers = pyqtSignal(int, int) # Used by the Track Model to update the passenger count of a train (trainId, newPassCount)
    train_model_update_direction = pyqtSignal(int, int) # Used by the Track Model to update the direction of a train (trainId, newDirection)
    train_model_receive_beacon_info = pyqtSignal(int, str, DoorSide) # TrainID, Station Name, DoorSide
    train_model_report_sp_failure = pyqtSignal(int, bool) # TrainID, failReport
    train_model_report_sb_failure = pyqtSignal(int, bool) # TrainID, failReport
    train_model_report_e_failure = pyqtSignal(int, bool) # TrainID, failReport
    train_model_resolve_failure = pyqtSignal(int) # TrainID
    train_model_receive_track_circuit = pyqtSignal(Line, int, TrackCircuit) # Used by the track model to send the track circuit to the train model (line, trainId, trackCircuit)

    # SWTrainController Signals
    swtrain_gui_toggle_cabin_lights = pyqtSignal(int) # TrainID
    swtrain_dispatch_train = pyqtSignal(float, float, bool) # command speed, current speed, authority
    swtrain_update_current_speed = pyqtSignal(int, float) # TrainID, current speed
    swtrain_update_command_speed = pyqtSignal(int, float) # TrainID, command speed
    swtrain_update_authority = pyqtSignal(int, bool) # TrainID, authority
    swtrain_cause_failure = pyqtSignal(bool, bool, bool) # Failures
    swtrain_pull_passenger_ebrake = pyqtSignal(int) # TrainID
    swtrain_gui_pull_ebrake = pyqtSignal(int) # TrainID
    swtrain_gui_release_ebrake = pyqtSignal(int) #TrainID
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
    swtrain_receive_beacon = pyqtSignal(int, Beacon) # TrainID, beacon
    swtrain_send_beacon_info = pyqtSignal(int, str, DoorSide) # TrainID, Station Name, DoorSide
    swtrain_receive_signal_pickup_failure = pyqtSignal(int, bool) # TrainID, signal_pickup_failure
    swtrain_receive_brake_failure = pyqtSignal(int, bool) # TrainID, brake_failure
    swtrain_receive_engine_failure = pyqtSignal(int, bool) # TrainID, engine_failure
    swtrain_resolve_failure = pyqtSignal(int) # TrainID

    # Track Model Signals
    trackmodel_dispatch_train = pyqtSignal(int, int, float, bool, Line, list) # Used by SWTrack Controller to send dispatch Train (train_id, command_speed, authority, Line, switches_arr(boolean))
    trackmodel_update_occupancy = pyqtSignal(int, Line, int, bool, int) # Used by train model to give track model info about a train's status on a particular block (trainId, Line, blockId, trainOrNot, travelDirection)
    trackmodel_update_command_speed = pyqtSignal(int, float) # Used by the track controller to update the command speed of a train (trainId, newSpeed)
    trackmodel_update_switch_positions = pyqtSignal(Line, int, bool) # Used by the track controller to update a switch positions (Line, switchNumberFromYard, switchPosition)
    trackmodel_update_authority = pyqtSignal(Line, int, bool) # Used by the track controller to update the authority of a train (trainId, newAuthority)
    trackmodel_update_gui = pyqtSignal() # used by the track model to tell me to update my gui
    trackmodel_update_passengers_exited = pyqtSignal(Line, int, int, int, int, int) # used by train model to communicate how many passengers left the train (Line, trainId, blockNumberOfStation, passengersExited, spaceAvailable, totalSeats)
    trackmodel_update_tickets_sold = pyqtSignal() # used to tell Track model to generate new tickets
    trackmodel_receive_track_circuit = pyqtSignal(Line, int, TrackCircuit) # Line, train_id, trackcircuit
# Single instance to be used by other modules
signals = SignalsClass()
