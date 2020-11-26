"""Module containing the definition for a track controller object"""

from src.SWTrackController.plc_components import Instruction, InstructionType
from src.signals import signals
from src.logger import get_logger

logger = get_logger(__name__)

class TrackController:
    """Object to represent a single track controller"""
    def __init__(self):

        # Tags in the plc program
        self.tags = {}

        self.program_name = ""
        self.task_list = []

    def run_program(self):
        """Runs the plc program"""
        for task in self.task_list:
            for rung in task[0]:
                rung_status = True

                for instruction in rung:
                    if rung_status:
                        rung_status = self.evaluate_instruction(instruction)
                    else:
                        if instruction.type == InstructionType.OTE:
                            self.tags[instruction.argument] = False

    def evaluate_instruction(self, instruction):
        """Evaluates the given instruction given the states of the tags

        :param Instruction instruction: Instruction to be evaluated

        :return: Result of the evaluation
        :rtype: bool
        """
        result = False

        if instruction.type == InstructionType.XIC:
            result = self.tags[instruction.argument]
        elif instruction.type == InstructionType.XIO:
            result = not self.tags[instruction.argument]
        elif (instruction.type == InstructionType.OTE) or \
             (instruction.type == InstructionType.OTL):
            self.tags[instruction.argument] = True
            result = True
        elif instruction.type == InstructionType.OTU:
            self.tags[instruction.argument] = False
            result = True
        else:
            assert False

        return result

    def download_program(self, compiled_program):
        """Constructs the plc program given the compiled output

        :param file compiled_program: File containing the compiler output
        """
        logger.debug("Downloading program in %s", compiled_program)

        for line in open(compiled_program, 'r'):
            splits = line.split()

            command = splits[0]

            if command == 'START_DOWNLOAD':
                self.program_name = splits[1]
            elif command == 'CREATE_TAG':
                self.tags.update({splits[1] : splits[2] == 'TRUE'})
            elif command == 'CREATE_TASK':
                # Assert that task is continuous???
                self.task_list.append([])
            elif command == 'CREATE_ROUTINE':
                self.task_list[-1].append([])
            elif command == 'CREATE_RUNG':
                self.task_list[-1][-1].append([])
            elif command == 'CREATE_INSTRUCTION':
                instruction = Instruction(InstructionType[splits[1]], splits[2])
                self.task_list[-1][-1][-1].append(instruction)
            elif command == 'END_DOWNLOAD':
                self.run_program()
            else:
                assert False, "Unknown command from the compiler"

    def get_tag_value(self, tag_name):
        """Gets a tag's value from inside the plc

        :param str tag_name: Name of the tag

        :return: Value of the tag
        :rtype: bool
        """
        # TODO(nns): Remove this try catch once complete
        try:
            return self.tags[tag_name]
        except KeyError:
            return None

    def set_tag_value(self, tag_name, value):
        """Sets a tag's value inside the plc

        :param str tag_name: Name of the tag
        :param bool value: Value to set to the tag to
        """
        try:
            self.tags[tag_name] = value
            signals.swtrack_update_gui.emit()
        except KeyError:
            logger.debug("Tag named %s not found", tag_name)

    def set_block_occupancy(self, block_id, occupied):
        """Sets the block occupancy tag for the given block

        :param int block_id: Id of the block
        :param bool occupied: Whether the block is now occupied or not
        """
        self.set_tag_value('b{}O'.format(block_id), occupied)

        # Run the program since tag values have been changed
        self.run_program()

    def get_authority_of_block(self, block_id):
        """Gets the authority tag for the given block

        :param int block_id: Id of the block in question

        :return: Whether a train on the block would be given authority
        :trype: bool
        """
        return self.get_tag_value("b{}A".format(block_id))

    def get_switch_position(self):
        """Gets the value of the switch tag in the controller

        :return: Value of the switch tag
        :rtype: bool
        """
        return self.get_tag_value("switch")

    def set_track_heater(self, status):
        """Method to set the track heater

        :param bool status: Whether heater should be on or off
        """
        self.set_tag_value('heater', status)

    def get_track_heater_status(self):
        """Method to whether the heater is on or off

        :return: Track heater status
        :rtype: bool
        """
        return self.get_tag_value("heater")

    def get_light_status(self):
        """Method to get the light status"""
        return self.get_tag_value("signal")

    def get_block_occupancy(self, block_id):
        """Method to get the block occupancy"""
        return self.get_tag_value("b{}O".format(block_id))

    def get_block_status(self, block_id):
        """Method to get a block's status"""
        return self.get_tag_value("b{}S".format(block_id))

    def get_railway_crossing(self, block_id):
        """Method to get the status of a railway crossing on the given block"""
        return self.get_tag_value("b{}RRX".format(block_id))

if __name__ == "__main__":
    raise Exception("Not to be run as a module")
