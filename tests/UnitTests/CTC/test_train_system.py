""" UNIT Testing for CTC Train System File """

import unittest
import sys

sys.path.insert(1, '.')
from src.CTC.train_system import ctc
from src.common_def import Line

class MyTestCase(unittest.TestCase):
    """ Testing for CTC Module """

    def test_init(self):
        """ Test Initialization """

        self.assertEqual(len(ctc.blocks_green_arr) == 150, True)
        self.assertEqual(len(ctc.blocks_red_arr) == 76, True)
        self.assertEqual(len(ctc.switches_green_arr) == 6, True)
        self.assertEqual(len(ctc.switches_red_arr) == 7, True)


    def test_trackocc(self):
        """ Test Setting Track Occupied """

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


    def test_switchset(self):
        """ Test Setting Switches """

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


    def test_dispatch(self):
        """ Test Setting Switches """

        # Test that the train array is empty
        self.assertEqual(len(ctc.trains_arr) == 0, True)
        self.assertEqual(len(ctc.train_numbers) == 0, True)

        # Dispatch a Train
        ctc.dispatch_train(10, Line.LINE_GREEN)

        # Test that train was dispatched
        self.assertEqual(len(ctc.trains_arr) == 1, True)
        self.assertEqual(len(ctc.train_numbers) == 1, True)

        # Check that the train number is 1
        self.assertEqual(ctc.trains_arr[0].train_id == 1, True)
        self.assertEqual(ctc.train_numbers[0] == 1, True)

        # Check that train is on green line and information is right

        self.assertEqual(ctc.trains_arr[0].line_on == Line.LINE_GREEN, True)
        self.assertEqual(ctc.trains_arr[0].destination_block == 10, True)
        self.assertEqual(ctc.trains_arr[0].command_speed == 70, True)
        self.assertEqual(ctc.trains_arr[0].authority == 3, True)
        self.assertEqual(ctc.trains_arr[0].index_on_route == 0, True)

        # Remove train from array
        ctc.trains_arr.pop()
        ctc.train_numbers.pop()

        # Test that train was removed
        self.assertEqual(len(ctc.trains_arr) == 0, True)
        self.assertEqual(len(ctc.train_numbers) == 0, True)

        # Dispatch another train
        ctc.dispatch_train(13, Line.LINE_RED)

        # Test that train was dispatched
        self.assertEqual(len(ctc.trains_arr) == 1, True)
        self.assertEqual(len(ctc.train_numbers) == 1, True)

        # Check that the train number is 2
        self.assertEqual(ctc.trains_arr[0].train_id == 2, True)
        self.assertEqual(ctc.train_numbers[0] == 2, True)

        # Check that train is on green line and information is right
        self.assertEqual(ctc.trains_arr[0].line_on == Line.LINE_RED, True)
        self.assertEqual(ctc.trains_arr[0].destination_block == 13, True)
        self.assertEqual(ctc.trains_arr[0].command_speed == 70, True)
        self.assertEqual(ctc.trains_arr[0].authority == 3, True)
        self.assertEqual(ctc.trains_arr[0].index_on_route == 0, True)

# Main function Checker
if __name__ == '__main__':
    unittest.main()
