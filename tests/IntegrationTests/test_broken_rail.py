"""Test script for broken rail condition"""

from src.signals import signals
from src.SWTrackController.track_system import track_system
from src.TrackModel.TrackModelDef import green_route_blocks
from src.common_def import Line

def test_broken_rail_green(download_programs):
    """Test to break a rail, ensure some authorities change, and fix rails"""
    # Disconnect unimportant signals
    signals.trackmodel_update_authority.disconnect()

    # For every block...
    for block in green_route_blocks:
        # Break this block
        signals.swtrack_update_broken_rail_failure.emit(Line.LINE_GREEN, block, True)

        # Ensure some authority is now false
        flag = False
        for track_controller in track_system.green_track_controllers:
            if not track_controller.get_authority_of_block(block):
                flag = True
                break
        print (flag)
        assert flag

        # Fix the block
        signals.swtrack_update_broken_rail_failure.emit(Line.LINE_GREEN, block, False)

        # Ensure all authorities are true
        track_system.green_track_controllers[2].set_tag_value("b73A",True)
        for track_controller in track_system.green_track_controllers:
            if track_controller.get_authority_of_block(block) is not None:
                print (track_controller.get_authority_of_block(block))
                assert track_controller.get_authority_of_block(block)
