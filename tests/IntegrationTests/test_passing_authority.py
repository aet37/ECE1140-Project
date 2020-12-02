"""Test for passing authority from the track controller to the track model"""

from src.signals import signals
from src.common_def import Line
from src.TrackModel.TrackModelDef import green_route_blocks, red_route_blocks
from src.CTC.train_system import ctc

def verify_authority(line, block_id, new_authority):
    """Verifies that the authority remains true"""
    if not new_authority:
        print(block_id)
    assert new_authority

def test_passing_authority_green(upload_tracks, download_programs):
    """Testing passing authority. It should always be true because only 1 train is being dispatched"""
    # Disconnect signals going to and from track controller
    signals.train_model_dispatch_train.disconnect()
    signals.train_model_update_command_speed.disconnect()
    signals.trackmodel_update_authority.disconnect()
    signals.update_occupancy.disconnect()

    # Connect to signal to verify
    signals.trackmodel_update_authority.connect(verify_authority)

    # Dispatch a train
    ctc.dispatch_train(38, Line.LINE_GREEN)

    signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, green_route_blocks[0], True)
    for previous_block, current_block in zip(green_route_blocks, green_route_blocks[1:]):
        # Simulate the train changing blocks
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, previous_block, False)
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_GREEN, current_block, True)

def test_passing_authority_red(upload_tracks, download_programs):
    """Testing passing authority. It should always be true because only 1 train is being dispatched"""
    # Disconnect signals going to and from track controller
    try:
        signals.train_model_dispatch_train.disconnect()
        signals.trackmodel_update_authority.disconnect()
        signals.update_occupancy.disconnect()
    except Exception:
        pass

    # Connect to signal to verify
    signals.trackmodel_update_authority.connect(verify_authority)

    # Dispatch a train
    ctc.dispatch_train(60, Line.LINE_RED)

    signals.trackmodel_update_occupancy.emit(0, Line.LINE_RED, red_route_blocks[0], True)
    for previous_block, current_block in zip(red_route_blocks, red_route_blocks[1:]):
        # Simulate the train changing blocks
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_RED, previous_block, False)
        signals.trackmodel_update_occupancy.emit(0, Line.LINE_RED, current_block, True)
