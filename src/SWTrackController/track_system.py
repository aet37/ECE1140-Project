"""Module for the track controller module"""

from serial.serialutil import SerialException
from src.common_def import Line, pairwise
from src.SWTrackController.track_controller import TrackController
from src.HWTrackController.hw_track_controller_connector import HWTrackCtrlConnector
from src.signals import signals
from src.logger import get_logger

logger = get_logger(__name__)

NUMBER_OF_GREEN_CONTROLLERS = 12
NUMBER_OF_RED_CONTROLLERS = 14

class TrackSystem:
    """Overarching class to coordinate the track controllers"""
    def __init__(self):
        self.green_track_controllers = []
        self.red_track_controllers = []

        # Create the track controllers on the green line
        # Try and create a hw controller for the first one
        try:
            self.green_track_controllers.append(HWTrackCtrlConnector())
            logger.info("Created a HW track controller instance")
        except SerialException:
            logger.info("No HW track controller found")
            self.green_track_controllers.append(TrackController())

        for _ in range(1, NUMBER_OF_GREEN_CONTROLLERS):
            self.green_track_controllers.append(TrackController())

        # Create the track controllers on the red line
        for _ in range(0, NUMBER_OF_RED_CONTROLLERS):
            self.red_track_controllers.append(TrackController())

        # Connect to signals
        signals.swtrack_dispatch_train.connect(self.swtrack_dispatch_train)
        signals.swtrack_update_occupancies.connect(self.swtrack_update_occupancies)
        signals.swtrack_set_track_heater.connect(self.swtrack_set_track_heater)

    def swtrack_dispatch_train(self, train_id, destination_block, suggested_speed, suggested_authority, line, route):
        """Method connected to the swtrack_dispatch_train signal"""
        logger.critical("Received swtrack_dispatch_train")

        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN else self.red_track_controllers

        # Set occupancy of first block
        track_controllers[0].set_block_occupancy(0, True)

        # Get the speed limit of the block and compare it against suggested_speed
        speed_limit = track_controllers[0].get_speed_limit_of_block(0)

        if suggested_speed > speed_limit:
            command_speed = speed_limit
        else:
            command_speed = suggested_speed

        # Check whether the plc program will give the train authority
        authority = track_controllers[0].get_authority_of_block(0)

        # Gather all of the switch positions in case they've changed
        switch_positions = []
        for track_controller_1, track_controller_2 in pairwise(track_controllers):
            # TODO(nns): Add safety architecture here
            switch_positions.append(track_controller_1.get_switch_position())

        # Send the to the track model and ctc
        for i, switch_position in enumerate(switch_positions):
            signals.trackmodel_update_switch_positions.emit(line, i, switch_position)

        if line == Line.LINE_GREEN:
            signals.update_green_switches.emit(switch_positions)
        else:
            signals.update_red_switches.emit(switch_positions)

        # Pass the dispatch train information to the Track Model
        signals.trackmodel_dispatch_train.emit(train_id, destination_block, command_speed, authority, line, route)

    def swtrack_update_occupancies(self, line, block_id, occupied):
        """Method connected to the swtrack_update_occupancies signal"""
        logger.critical("Received swtrack_update_occupancies")

        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN else self.red_track_controllers

        # Set the occupancy of the specified block. This operation will only be
        # successful for the track controllers that operate the block
        for track_controller in track_controllers:
            # TODO(nns): Possibly add safety architecture here
            track_controller.set_block_occupancy(block_id, occupied)

        # Forward this information to the CTC
        signals.update_occupancy.emit(line, block_id, occupied)

    def swtrack_set_track_heater(self, line, status):
        """Method connected to the swtrack_set_track_heater signal"""
        logger.critical("Received swtrack_set_track_heater")

        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN else self.red_track_controllers

        # Turn all the heaters on/off
        for track_controller in track_controllers:
            track_controller.set_track_heater(status)


track_system = TrackSystem()
