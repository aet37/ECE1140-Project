"""
    @file CTCDef.py

    @brief Declaration of Structs and Enums used in CTC

    @author Andrew Toader

    @date 10.01.2020
"""

from src.Common.common_def import *

"""
	@struct Train

	@brief Structure that holds data about a single train (id, command speed, authority, destination block)
"""
class Train:
	def __init__(self, id_n, block, line):
		self.train_id = id_n
		self.command_speed = 0
		self.authority = 0
		self.destination_block = block
		self.line_on = line
		self.index_on_route = 0
		self.route_switches_arr = []


"""
	@struct Track

	@brief Structure that holds data about a single track (open, occupied)
"""
class Track:
	def __init__(self):
		self.open = True
		self.occupied = False

"""
	@struct Switch

	@brief Structure that holds data about a single Switch (pointing to)

	@note -1 denotes yard
"""
class Switch:
	def __init__(self, less, greater):
		self.less_block = less
		self.greater_block = greater
		self.pointing_to = less

	def TrackSwitchToString(self):
		if self.pointing_to == -1:
			to_return = 'Yrd'
		elif self.pointing_to < 10:
			to_return = '00'
			to_return = to_return + str(self.pointing_to)
		elif self.pointing_to < 100:
			to_return = '0'
			to_return = to_return + str(self.pointing_to)
		else:
			to_return = str(self.pointing_to)
		return to_return

# Do Not allow to be run as Main Module
if __name__ == "__main__":
	raise Exception("Not to be run as a module")