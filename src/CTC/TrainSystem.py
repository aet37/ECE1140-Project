"""
	@file TrainSystem.hpp

	@brief Declaration of the TrainSystem class; will run the CTC module

	@author Andrew Toader

	@date 10.01.2020
"""
import sys

from src.CTC.CTCDef import *

"""
	@class TrainSystem

	@brief Singleton class responsible for running vital operations of the CTC
	
	@members 
		@li train_numbers
		@li trains_arr
		@li blocks_green_arr
		@li blocks_red_arr
		@li switches_green_arr
		@li switches_red_arr
		@li green_route_blocks
		@li green_route_switches
		@li red_route_blocks
		@li red_route_switches
		
	@methods
		@li ImportTrackLayout
		@li DispatchTrain
		@li ReturnOccupancies
		@li ReturnSwitchPositions
		
"""


class TrainSystem:
	def __init__(self):
		self.ImportTrackLayout()
		self.next_train_num = 1
		self.train_numbers = []
		self.trains_arr = []
		self.green_route_blocks = [-1, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
		                           82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84,
		                           83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
		                           112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
		                           129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145,
		                           146, 147, 148, 149, 150, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15,
		                           14, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
		                           22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
		                           43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, -1]
		self.green_route_switches = [0, 0, 0, 1, 1, 1, 0, 1, 0, 0]
		self.red_route_blocks = [-1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75,
		                         74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51,
		                         52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46,
		                         45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,
		                         23, 22, 21, 20, 19, 18, 17, 16, 1, 2, 3, 4, 5, 6, 7, 8, -1]
		self.red_route_switches = [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]

	"""
		@brief Import the layout of the track
		
		@param[out] updates green and red blocks and switches
		
		@return None
	"""

	def ImportTrackLayout(self):
		self.blocks_green_arr = []
		self.blocks_red_arr = []
		self.switches_green_arr = []
		self.switches_red_arr = []

		# Initialize red blocks
		for i in range(76):
			self.blocks_red_arr.append(Track())
		# Initialize green blocks
		for i in range(150):
			self.blocks_green_arr.append(Track())

		# Create Green Switches
		sw1 = Switch(1, 12)
		sw2 = Switch(30, 150)
		sw3 = Switch(-1, 59)
		sw4 = Switch(-1, 61)
		sw5 = Switch(76, 101)
		sw6 = Switch(86, 100)
		self.switches_green_arr = [sw1, sw2, sw3, sw4, sw5, sw6]

		# Create Red Switches
		rsw1 = Switch(-1, 8)
		rsw2 = Switch(1, 15)
		rsw3 = Switch(28, 76)
		rsw4 = Switch(32, 72)
		rsw5 = Switch(39, 71)
		rsw6 = Switch(43, 67)
		rsw7 = Switch(53, 66)
		self.switches_red_arr = [rsw1, rsw2, rsw3, rsw4, rsw5, rsw6, rsw7]

	"""
		@brief Create(dispatch) a new train by creating the Train object then adding it to the class member vector

		@param[in]	block_to
		@param[in]  line_on

		@return pointer to newly created Train struct
	"""

	def DispatchTrain(self, block_to, line):
		# Create the train which will dispatch
		temp_train = Train(self.next_train_num, block_to, line)

		# Give Train Speed and Authority (blocks, km/hr)
		temp_train.authority = 3
		temp_train.command_speed = 55

		# Add train to this array
		self.trains_arr.append(temp_train)
		self.train_numbers.append(self.next_train_num)

		# Increment the next train number counter
		self.next_train_num += 1

	"""
		@breif Function which returns an array of track occupancies which the CTC GUI can use to dispaly on the screen
		
		@param[in]  line to return track occupancies
		
		@return array of boolean values
	"""

	def ReturnOccupancies(self, line):
		to_send = []
		if line == Line.LINE_GREEN:
			for i in range(len(self.blocks_green_arr)):
				to_send.append(self.blocks_green_arr[i].occupied)
		elif line == Line.LINE_RED:
			for i in range(len(self.blocks_red_arr)):
				to_send.append(self.blocks_red_arr[i].occupied)
		else:
			raise Exception('CTC : TrainSystem.ReturnOccupancies recieved an erronious input')
		return to_send

	"""
		@breif Function which returns an array of track occupancies which the CTC GUI can use to dispaly on the screen

		@param[in]  line to return track occupancies

		@return array of boolean values
	"""

	def ReturnSwitchPositions(self, line):
		to_send = []
		if line == Line.LINE_GREEN:
			for i in range(len(self.switches_green_arr)):
				to_send.append(self.switches_green_arr[i].TrackSwitchToString())
		elif line == Line.LINE_RED:
			for i in range(len(self.switches_red_arr)):
				to_send.append(self.switches_red_arr[i].TrackSwitchToString())
		else:
			raise Exception('CTC : TrainSystem.ReturnSwitchPositions recieved an erronious input')
		return to_send


# Define a TrainSystem object to use; acts as equivalent of singleton class
ctc = TrainSystem()
