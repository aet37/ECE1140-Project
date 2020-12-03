"""Test for passing occupancy from the track model, through the controller, to the ctc"""

from src.signals import signals
from src.common_def import Line
from src.TrackModel.TrackModelDef import green_route_blocks, red_route_blocks
from src.SWTrackController.track_system import track_system
from src.CTC.train_system import ctc

def test_passing_occupancy(upload_tracks, download_programs):
    """Testing passing occupancy"""
    # Disconnect signals going to train model
    signals.train_model_dispatch_train.disconnect()
    signals.train_model_update_authority.disconnect()
    signals.train_model_update_command_speed.disconnect()
    signals.train_model_update_direction.disconnect()

    # Dispatch a train
    ctc.dispatch_train(38, Line.LINE_GREEN)

    signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, green_route_blocks[0], True, 1)
    for previous_block, current_block in zip(green_route_blocks, green_route_blocks[1:]):
        # Simulate the train changing blocks
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, previous_block, False, 1)
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, current_block, True, 1)

        # Verify it got to the ctc
        assert current_block in track_system.green_occupied_blocks
        assert previous_block not in track_system.green_occupied_blocks

    # Dispatch a train
    ctc.dispatch_train(60, Line.LINE_RED)

    signals.trackmodel_update_occupancy.emit(1, Line.LINE_RED, red_route_blocks[0], True, 1)
    for previous_block, current_block in zip(red_route_blocks, red_route_blocks[1:]):
        # Simulate the train changing blocks
        signals.trackmodel_update_occupancy.emit(1, Line.LINE_RED, previous_block, False, 1)
        signals.trackmodel_update_occupancy.emit(1, Line.LINE_RED, current_block, True, 1)

        # Verify it got to the ctc
        assert current_block in track_system.red_occupied_blocks
        assert previous_block not in track_system.red_occupied_blocks
