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
        self.green_occupied_blocks = []
        self.red_occupied_blocks = []
        self.suggested_speeds = []

        for i in range(0, NUMBER_OF_GREEN_CONTROLLERS):
            if i == 5:
                # Create the track controllers on the green line
                # Try and create a hw controller for the first one
                try:
                    self.green_track_controllers.append(HWTrackCtrlConnector())
                    logger.info("Created a HW track controller instance")
                except SerialException:
                    logger.info("No HW track controller found")
                    self.green_track_controllers.append(TrackController())
            else:
                self.green_track_controllers.append(TrackController())

        # Create the track controllers on the red line
        for _ in range(0, NUMBER_OF_RED_CONTROLLERS):
            self.red_track_controllers.append(TrackController())

        # Connect to signals
        signals.swtrack_dispatch_train.connect(self.swtrack_dispatch_train)
        signals.swtrack_update_occupancies.connect(self.swtrack_update_occupancies)
        signals.swtrack_set_track_heater.connect(self.swtrack_set_track_heater)
        signals.swtrack_update_broken_rail_failure.connect(self.swtrack_update_failure)
        signals.swtrack_update_power_failure.connect(self.swtrack_update_failure)
        signals.swtrack_update_track_circuit_failure.connect(self.swtrack_update_failure)
        signals.swtrack_force_authority_reevaluation.connect(self.force_authority_reevaluation)

    def swtrack_dispatch_train(self, train_id, destination_block, suggested_speed,
                               suggested_authority, line, route):
        """Method connected to the swtrack_dispatch_train signal"""
        logger.critical("Received swtrack_dispatch_train")

        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN \
                                                         else self.red_track_controllers

        # Set occupancy of first block
        track_controllers[0].set_block_occupancy(0, True)

        # Save the suggested speed for this train to compare to in the future
        self.suggested_speeds.append(suggested_speed)

        # Get the speed limit of the block and compare it against suggested_speed
        speed_limit = self.get_speed_limit_of_block(line, 0)

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

        # TODO (ljk): Remove this once plc programs are autouploaded!
        if authority is None:
            authority = True

        # Pass the dispatch train information to the Track Model
        signals.trackmodel_dispatch_train.emit(train_id, destination_block, command_speed,
                                               authority, line, route)

    # pylint: disable=too-many-branches
    def swtrack_update_occupancies(self, train_id, line, block_id, occupied):
        """Method connected to the swtrack_update_occupancies signal"""
        logger.debug("Received swtrack_update_occupancies")

        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN \
                                                         else self.red_track_controllers
        occupied_blocks = self.green_occupied_blocks if line == Line.LINE_GREEN \
                                                     else self.red_occupied_blocks

        # Update the occupied block list
        if occupied:
            occupied_blocks.append(block_id)
        else:
            occupied_blocks.remove(block_id)

        # Set the occupancy of the specified block. This operation will only be
        # successful for the track controllers that operate the block
        final_authorities = [True for _ in range(len(occupied_blocks))]
        switch_positions = [False for _ in range(int(len(track_controllers) / 2))]
        for i, track_controller in enumerate(track_controllers):
            # TODO(nns): Possibly add safety architecture here
            track_controller.set_block_occupancy(block_id, occupied)

            # Update switch positions
            switch_position = track_controller.get_switch_position()
            signals.trackmodel_update_switch_positions.emit(
                line,
                self.convert_switch_position_ordering(line, int(i / 2)),
                switch_position
            )
            switch_positions[self.convert_switch_position_ordering(line, int(i / 2))] = switch_position

            # Go through occupied blocks and update their authorities
            for j, block in enumerate(occupied_blocks):
                new_authority = track_controller.get_authority_of_block(block)
                if new_authority is not None:
                    # It only takes one false authority to stop the train
                    if not new_authority:
                        final_authorities[j] = False
                    logger.debug("New authority of {} found in track controller {} for train "
                                 "{} and block {}".format(new_authority, i, train_id, block))

        if line == Line.LINE_GREEN:
            signals.update_green_switches.emit(switch_positions)
        else:
            signals.update_red_switches.emit(switch_positions)

        # Emit the final updated authorities for the occupied blocks
        for final_authority, block in zip(final_authorities, occupied_blocks):
            signals.trackmodel_update_authority.emit(line, block, final_authority)

        # Forward this information to the CTC
        if block_id != 0:
            signals.update_occupancy.emit(line, block_id, occupied)

        # Update command speed now since speed limit may have changed
        if occupied:
            speed_limit = self.get_speed_limit_of_block(line, block_id)

            if self.suggested_speeds[train_id] > speed_limit:
                command_speed = speed_limit
            else:
                command_speed = self.suggested_speeds[train_id]

            signals.trackmodel_update_command_speed.emit(train_id, command_speed)

    def swtrack_set_track_heater(self, line, status):
        """Method connected to the swtrack_set_track_heater signal"""
        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN \
                                                         else self.red_track_controllers

        # Turn all the heaters on/off
        for track_controller in track_controllers:
            track_controller.set_track_heater(status)

    def swtrack_update_failure(self, line, block_id, status):
        """Simulates a broken or fixed rail

        :param Line line: Line on which the block is
        :param int block_id: Block that will be broken
        :param bool status: Whether the track is being broken or fixed
        """
        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN \
                                                         else self.red_track_controllers
        occupied_blocks = self.green_occupied_blocks if line == Line.LINE_GREEN \
                                                     else self.red_occupied_blocks

        final_authorities = [True for _ in range(len(occupied_blocks))]
        for track_controller in track_controllers:
            # If this track controller has authority of this block
            if track_controller.get_authority_of_block(block_id) is not None:

                # Count that number of failures that have been induced
                if status:
                    track_controller.number_of_failures += 1

                    # Only take action if this is the first
                    if track_controller.number_of_failures == 1:
                        track_controller.set_broken_rail(status)
                else:
                    track_controller.number_of_failures -= 1

                    # Only take action if this is the last
                    if track_controller.number_of_failures == 0:
                        track_controller.set_broken_rail(status)

            # Go through occupied blocks and update their authorities
            for j, block in enumerate(occupied_blocks):
                new_authority = track_controller.get_authority_of_block(block)
                if new_authority is not None:
                    # It only takes one false authority to stop the train
                    if not new_authority:
                        final_authorities[j] = False

        # Emit the final updated authorities for the occupied blocks
        for final_authority, block in zip(final_authorities, occupied_blocks):
            signals.trackmodel_update_authority.emit(line, block, final_authority)

    def force_authority_reevaluation(self, line):
        """Forces all occupied blocks to have their authorities reevaluated"""
        logger.info("Force reevaluation of authorities")
        # Get the correct list of track controllers based on the line
        track_controllers = self.green_track_controllers if line == Line.LINE_GREEN \
                                                         else self.red_track_controllers
        occupied_blocks = self.green_occupied_blocks if line == Line.LINE_GREEN \
                                                     else self.red_occupied_blocks

        final_authorities = [True for _ in range(len(occupied_blocks))]
        for track_controller in track_controllers:

            # Go through occupied blocks and update their authorities
            for j, block in enumerate(occupied_blocks):
                new_authority = track_controller.get_authority_of_block(block)
                if new_authority is not None:
                    # It only takes one false authority to stop the train
                    if not new_authority:
                        final_authorities[j] = False

        # Emit the final updated authorities for the occupied blocks
        for final_authority, block in zip(final_authorities, occupied_blocks):
            signals.trackmodel_update_authority.emit(line, block, final_authority)


    @staticmethod
    def get_speed_limit_of_block(line, block_id):
        """Maps a block number to its speed limit

        :param Line line: Line that the block is on
        :param int block_id: Id of the block in question

        :return: Speed limit of the block
        :rtype: float
        """
        speed_limit = 0.0
        if line == Line.LINE_GREEN:
            if (block_id in range(0, 13)) or \
               (block_id in range(67, 77)):
                speed_limit = 40.0
            elif block_id in range(17, 21):
                speed_limit = 60.0
            elif (block_id in range(27, 63)) or \
                 (block_id in range(110, 117)):
                speed_limit = 30.0
            elif block_id in range(86, 101):
                speed_limit = 25.0
            elif block_id == 101:
                speed_limit = 26.0
            elif block_id in range(102, 110):
                speed_limit = 28.0
            elif block_id in range(117, 122):
                speed_limit = 15.0
            elif block_id in range(122, 151):
                speed_limit = 20.0
            else:
                speed_limit = 70.0
        else:
            if block_id in range(0, 17):
                speed_limit = 40.0
            elif (block_id == 17) or \
                 (block_id in range(21, 24)) or \
                 (block_id in range(51, 77)):
                speed_limit = 55.0
            elif block_id in range(59, 61):
                speed_limit = 60
            else:
                speed_limit = 70.0

        return speed_limit
    # pylint: enable=too-many-branches

    @staticmethod
    def convert_switch_position_ordering(line, original_index):
        """Converts the index of a switch from the track controller's ordering to everyone else's"""
        new_index = None

        if line == Line.LINE_GREEN:
            if original_index == 0:
                new_index = 3
            elif original_index == 1:
                new_index = 4
            elif original_index == 2:
                new_index = 5
            elif original_index == 3:
                new_index = 1
            elif original_index == 4:
                new_index = 0
            elif original_index == 5:
                new_index = 2
        else:
            new_index = original_index

        assert new_index is not None
        return new_index

track_system = TrackSystem()
