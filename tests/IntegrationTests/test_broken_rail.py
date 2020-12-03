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
        track_system.green_track_controllers[2].set_tag_value("b74A",True)
        track_system.green_track_controllers[2].set_tag_value("b75A",True)
        track_system.green_track_controllers[2].set_tag_value("b76A",True)
        track_system.green_track_controllers[2].set_tag_value("b77A",True)
        track_system.green_track_controllers[2].set_tag_value("b78A",True)
        track_system.green_track_controllers[2].set_tag_value("b79A",True)
        track_system.green_track_controllers[2].set_tag_value("b80A",True)
        track_system.green_track_controllers[2].set_tag_value("b81A",True)
        track_system.green_track_controllers[2].set_tag_value("b82A",True)
        track_system.green_track_controllers[2].set_tag_value("b83A",True)
        track_system.green_track_controllers[2].set_tag_value("b84A",True)
        track_system.green_track_controllers[2].set_tag_value("b85A",True)
        track_system.green_track_controllers[2].set_tag_value("b86A",True)
        track_system.green_track_controllers[2].set_tag_value("b87A",True)
        track_system.green_track_controllers[2].set_tag_value("b88A",True)
        track_system.green_track_controllers[2].set_tag_value("b89A",True)
        track_system.green_track_controllers[2].set_tag_value("b90A",True)
        track_system.green_track_controllers[2].set_tag_value("b91A",True)
        track_system.green_track_controllers[2].set_tag_value("b92A",True)
        track_system.green_track_controllers[2].set_tag_value("b93A",True)
        track_system.green_track_controllers[2].set_tag_value("b94A",True)
        track_system.green_track_controllers[2].set_tag_value("b95A",True)
        track_system.green_track_controllers[2].set_tag_value("b96A",True)
        track_system.green_track_controllers[2].set_tag_value("b97A",True)
        track_system.green_track_controllers[2].set_tag_value("b98A",True)
        track_system.green_track_controllers[2].set_tag_value("b99A",True)
        track_system.green_track_controllers[2].set_tag_value("b100A",True)
        track_system.green_track_controllers[2].set_tag_value("b101A",True)
        track_system.green_track_controllers[2].set_tag_value("b102A",True)
        track_system.green_track_controllers[2].set_tag_value("b103A",True)
        track_system.green_track_controllers[2].set_tag_value("b104A",True)
        track_system.green_track_controllers[2].set_tag_value("b105A",True)
        track_system.green_track_controllers[2].set_tag_value("b106A",True)
        track_system.green_track_controllers[2].set_tag_value("b107A",True)
        track_system.green_track_controllers[2].set_tag_value("b108A",True)
        track_system.green_track_controllers[2].set_tag_value("b109A",True)
        track_system.green_track_controllers[2].set_tag_value("b110A",True)
        track_system.green_track_controllers[2].set_tag_value("b111A",True)
        track_system.green_track_controllers[2].set_tag_value("b112A",True)
        track_system.green_track_controllers[2].set_tag_value("b113A",True)
        track_system.green_track_controllers[2].set_tag_value("b114A",True)
        track_system.green_track_controllers[2].set_tag_value("b115A",True)
        track_system.green_track_controllers[2].set_tag_value("b116A",True)
        track_system.green_track_controllers[2].set_tag_value("b117A",True)
        track_system.green_track_controllers[2].set_tag_value("b118A",True)
        track_system.green_track_controllers[2].set_tag_value("b119A",True)
        track_system.green_track_controllers[2].set_tag_value("b120A",True)
        track_system.green_track_controllers[2].set_tag_value("b121A",True)
        track_system.green_track_controllers[2].set_tag_value("b122A",True)
        track_system.green_track_controllers[2].set_tag_value("b123A",True)
        track_system.green_track_controllers[2].set_tag_value("b124A",True)
        track_system.green_track_controllers[2].set_tag_value("b125A",True)
        track_system.green_track_controllers[2].set_tag_value("b126A",True)
        track_system.green_track_controllers[2].set_tag_value("b127A",True)
        track_system.green_track_controllers[2].set_tag_value("b128A",True)
        track_system.green_track_controllers[2].set_tag_value("b129A",True)
        track_system.green_track_controllers[2].set_tag_value("b130A",True)
        track_system.green_track_controllers[2].set_tag_value("b131A",True)
        track_system.green_track_controllers[2].set_tag_value("b132A",True)
        track_system.green_track_controllers[2].set_tag_value("b133A",True)
        track_system.green_track_controllers[2].set_tag_value("b134A",True)
        track_system.green_track_controllers[2].set_tag_value("b135A",True)
        track_system.green_track_controllers[2].set_tag_value("b136A",True)
        track_system.green_track_controllers[2].set_tag_value("b137A",True)
        track_system.green_track_controllers[2].set_tag_value("b138A",True)
        track_system.green_track_controllers[2].set_tag_value("b139A",True)
        track_system.green_track_controllers[2].set_tag_value("b140A",True)
        track_system.green_track_controllers[2].set_tag_value("b141A",True)
        track_system.green_track_controllers[2].set_tag_value("b142A",True)
        track_system.green_track_controllers[2].set_tag_value("b143A",True)
        track_system.green_track_controllers[2].set_tag_value("b144A",True)
        track_system.green_track_controllers[2].set_tag_value("b145A",True)
        track_system.green_track_controllers[2].set_tag_value("b146A",True)
        track_system.green_track_controllers[2].set_tag_value("b147A",True)
        track_system.green_track_controllers[2].set_tag_value("b148A",True)
        track_system.green_track_controllers[2].set_tag_value("b149A",True)
        track_system.green_track_controllers[2].set_tag_value("b150A",True)
        for track_controller in track_system.green_track_controllers:
            if track_controller.get_authority_of_block(block) is not None:
                print (track_controller.get_authority_of_block(block))
                assert track_controller.get_authority_of_block(block)
