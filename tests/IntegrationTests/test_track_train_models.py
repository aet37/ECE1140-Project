"""Tests for interactions between the train model and sw train controller"""

import sys
sys.path.insert(1, '.')
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system
from src.timekeeper import timekeeper
import time
from src.TrackModel.TrackModelDef import *
from src.TrainModel.TrainCatalogue import *
from src.SWTrackController.track_system import track_system
import polling
from traceback import print_stack

def test_occupancy(start_app):
    """Testing the power loop"""
    signals.swtrack_update_occupancies.disconnect()
    # Dispatch a train from the train model
    signals.swtrack_dispatch_train.emit(0, 38, 15, 0, Line.LINE_GREEN, [0, 0, 0, 1, 1, 1, 0, 1, 0, 0])

    # Set kp and ki
    signals.swtrain_gui_set_kp_ki.emit(0, 100, 100)

    # Set time to ten times wall clock speed
    timekeeper.time_factor = 0.05

    # # Wait until speed is reached
    # while(True):
    #     time.sleep(0.05)
    #     signals.swtrain_time_trigger.emit()
    #     if round(control_system.p_controllers[0].current_speed, 2) == 9.32:
    #         break
    #     assert round(control_system.p_controllers[0].current_speed, 2) < 9.32
    #     assert round(train_catalogue.m_trainList[0].m_currentSpeed, 2) < 9.32

    #     if timekeeper.current_time_min > 10:
    #         assert False

    # Check to make sure speed is maintained
    # minutes = timekeeper.current_time_min
    # while(True):
    #     assert round(control_system.p_controllers[0].current_speed, 2) == 9.32
    #     assert round(train_catalogue.m_trainList[0].m_currentSpeed, 2) == 9.32
    #     if (timekeeper.current_time_min == (minutes + 5)):
    #         break

    theTrack = getTrack("Green")

    while(train_catalogue.m_trainList[0].m_route[0] == 62):
        signals.swtrain_time_trigger.emit()

    while (train_catalogue.m_trainList[0].m_route[0] == 63):
        signals.swtrain_time_trigger.emit()
        # asserting that trainId of block is correct
        polling.poll(polling_function, step=0.1, args=(theTrack,), timeout=100)

    while (train_catalogue.m_trainList[0].m_route[0] == 64):
        signals.swtrain_time_trigger.emit()
        # asserting that trainId of block is correct
        polling.poll(polling_function, step=0.1, args=(theTrack,), timeout=100)

    while (train_catalogue.m_trainList[0].m_route[0] == 65):
        signals.swtrain_time_trigger.emit()
        # asserting that trainId of block is correct
        polling.poll(polling_function, step=0.1, args=(theTrack,), timeout=100)


def polling_function(theTrack):
    x = train_catalogue.m_trainList[0].m_route[0]
    signals.swtrain_time_trigger.emit()
    return theTrack.getBlock(x).blockOccupied == 0 and theTrack.getBlock(x - 1).blockOccupied == -1
