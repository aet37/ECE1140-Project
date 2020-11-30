"""Test for passing occupancy from the track model, through the controller, to the ctc"""

from src.signals import signals
from src.common_def import Line
from src.TrackModel.TrackModelDef import green_route_blocks
from src.SWTrackController.track_system import track_system
from src.CTC.train_system import ctc

def test_passing_occupancy(upload_tracks):
    """Testing passing occupancy"""
    # Disconnect signals going to train model
    signals.train_model_dispatch_train.disconnect()
    signals.train_model_update_authority.disconnect()
    signals.train_model_update_command_speed.disconnect()

    # Dispatch a train
    ctc.dispatch_train(38, Line.LINE_GREEN)

    signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, green_route_blocks[0], True)
    for previous_block, current_block in zip(green_route_blocks, green_route_blocks[1:]):
        print(previous_block, current_block)
        # Simulate the train changing blocks
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, previous_block, False)
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, current_block, True)

        # Verify it got to the ctc
        assert current_block in track_system.occupied_blocks
        assert previous_block not in track_system.occupied_blocks
