"""Module containing the definition for a track controller object"""

from src.logger import get_logger

logger = get_logger(__name__)

class TrackController:
    """Object to represent a single track controller"""
    def __init__(self):

        # Tags in the plc program
        self.tags = {}

    def run_program(self):
        """"""
        pass

    def download_program(self, compiled_program):
        """Constructs the plc program given the compiled output
        
        :param file compiled_program: File containing the compiler output
        """
        logger.debug("Downloading program in %s", compiled_program)
        pass

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
            return True

    def set_tag_value(self, tag_name, value):
        """Sets a tag's value inside the plc

        :param str tag_name: Name of the tag
        :param bool value: Value to set to the tag to
        """
        try:
            self.tags[tag_name] = value
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

    def get_speed_limit_of_block(self, block_id):
        """Gets the speed limit of the given block

        :param int block_id: Id of the block in question

        :return: Speed limit of the block in km/hr
        :rtype: float
        """
        # TODO(nns): Pass back actual speed limit
        return 45.0

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

if __name__ == "__main__":
    raise Exception("Not to be run as a module")
