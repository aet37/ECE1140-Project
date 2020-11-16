"""
	UNIT Testing for CTC Train System File

	Author: Andrew Toader

	Date: 15 November 2020
"""

import unittest
from TrainSystem import *

"""
	Unit Testing Class
"""
class MyTestCase(unittest.TestCase):

	"""
		Test Initialization
	"""
	def test_init(self):
		self.assertEqual(len(ctc.blocks_green_arr) == 150, True)
		self.assertEqual(len(ctc.blocks_red_arr) == 76, True)
		self.assertEqual(len(ctc.switches_green_arr) == 6, True)
		self.assertEqual(len(ctc.switches_red_arr) == 7, True)

	"""
		Test Setting Track Occupied
	"""
	def test_trackocc(self):
		# Make sure they are initialized to not occupied
		self.assertEqual(ctc.blocks_green_arr[1].occupied, False)
		self.assertEqual(ctc.blocks_red_arr[1].occupied, False)

		# Make them occupied
		ctc.blocks_green_arr[1].occupied = True
		ctc.blocks_red_arr[1].occupied = True

		# Make sure they show up occupied
		self.assertEqual(ctc.blocks_green_arr[1].occupied, True)
		self.assertEqual(ctc.blocks_red_arr[1].occupied, True)

		# Make sure that that operation did not cause any other blocks to become occupied
		self.assertEqual(ctc.blocks_green_arr[3].occupied, False)
		self.assertEqual(ctc.blocks_red_arr[5].occupied, False)

	"""
		Test Setting Switches
	"""
	def test_switchset(self):
		# Test initialized correctly
		self.assertEqual(ctc.switches_green_arr[0].pointing_to == 1, True)
		self.assertEqual(ctc.switches_red_arr[2].pointing_to == 28, True)

		# Test changing pointing
		ctc.switches_green_arr[0].pointing_to = ctc.switches_green_arr[0].greater_block
		ctc.switches_red_arr[2].pointing_to = ctc.switches_red_arr[2].greater_block

		# Test pointing to right block after switched
		self.assertEqual(ctc.switches_green_arr[0].pointing_to == 12, True)
		self.assertEqual(ctc.switches_red_arr[2].pointing_to == 76, True)

		# Test that it did not affect any other block
		self.assertEqual(ctc.switches_green_arr[3].pointing_to == -1, True)
		self.assertEqual(ctc.switches_red_arr[4].pointing_to == 39, True)

# Main function Checker
if __name__ == '__main__':
	unittest.main()
