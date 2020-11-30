"""Tests for interactions between the train model and sw train controller"""

import sys
sys.path.insert(1, '.')
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.timekeeper import timekeeper
from src.TrackModel.TrackModelDef import *
from src.TrainModel.TrainCatalogue import *
import polling

def test_occupancy(upload_tracks, download_programs, start_timekeeper):
    """Testing the power loop"""
    # Disconnect unimportant signals
    signals.swtrack_update_occupancies.disconnect()

    # Dispatch a train from the train model
    signals.swtrack_dispatch_train.emit(0, 38, 15, 0, Line.LINE_GREEN, [0, 0, 0, 1, 1, 1, 0, 1, 0, 0])

    # Set kp and ki
    signals.swtrain_gui_set_kp_ki.emit(0, 100, 100)

    # Set time to ten times wall clock speed
    timekeeper.time_factor = 0.05

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
