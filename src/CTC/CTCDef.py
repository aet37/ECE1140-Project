from src.common_def import *

class Train:
	""" Structure that holds data about a single train (id, command speed, authority, destination block) """
	def __init__(self, id_n, block, line):
		self.train_id = id_n
		self.command_speed = 0
		self.authority = 0
		self.destination_block = block
		self.line_on = line
		self.index_on_route = 0
		self.route_switches_arr = []
		self.route_blocks_arr = []


class InterruptTrain:
	""" Used to hold information about a train while it is waiting to be dispatched """
	def __init__(self, block, line, hr, mn):
		self.destination_block = block
		self.line_on = line
		self.hour = hr
		self.min = mn

class Track:
	""" Structure that holds data about a single track (open, occupied) """

	def __init__(self):
		self.open = True
		self.occupied = False

class Switch:
	""" Structure that holds data about a single Switch (pointing to) """

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