""" Holds CTC main class """

import copy

from src.CTC.ctc_def import Train, Track, Switch
from src.common_def import Line
from src.signals import signals

class TrainSystem:
    """ class responsible for running vital operations of the CTC """
    def __init__(self):
        self.import_track_layout()
        self.next_train_num = 1
        self.throughput = 0
        self.train_numbers = []
        self.trains_arr = []
        self.green_route_blocks = [-1, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                                   77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
                                   93, 94, 95, 96, 97, 98, 99, 100, 85, 84, 83, 82, 81, 80, 79, 78,
                                   77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                                   113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
                                   139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 29,
                                   28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,
                                   1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                                   19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                                   35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                   51, 52, 53, 54, 55, 56, 57, 58, -1]
        self.green_route_blocks_multiple = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
                                            76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                                            90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84,
                                            83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105,
                                            106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
                                            117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
                                            128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
                                            139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
                                            150, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18,
                                            17, 16, 15, 14, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                            12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                                            26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                                            40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
                                            54, 55, 56, 57, 58]
        self.green_blocks_inter = [59, 60, 61]
        self.green_route_switches = [0, 0, 0, 1, 1, 1, 0, 1, 0, 0]
        self.green_route_switches_inter = [1, 0, 0, 1, 1, 1, 0, 1, 0, 1]

        self.red_route_blocks = [-1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23,
                                 24, 25, 26, 27, 76, 75, 74, 73, 72, 33, 34, 35, 36, 37, 38, 71,
                                 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
                                 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48,
                                 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32,
                                 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,
                                 1, 2, 3, 4, 5, 6, 7, 8, 9, -1]
        self.red_route_blocks_multiple = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75,
                                         74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67,
                                         44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                                         58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48,
                                         47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34,
                                         33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20,
                                         19, 18, 17, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.red_blocks_inter = [10, 11, 12, 13, 14, 15]
        self.red_route_switches = [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0]
        self.red_route_switches_inter = [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]

        # Signal Connections
        signals.update_occupancy.connect(self.update_blocks)
        signals.update_green_switches.connect(self.update_g_switches)
        signals.update_red_switches.connect(self.update_r_switches)
        signals.update_throughput.connect(self.update_throughput)
        signals.dispatch_scheduled_train.connect(self.dispatch_train)


    def import_track_layout(self):
        """ Import the layout of the track """
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

    def dispatch_train(self, block_to, line):
        """ Create(dispatch) a new train by creating the Train and adding to member list """

        # Create the train which will dispatch
        temp_train = Train(self.next_train_num, block_to, line)

        # Give Train Speed and Authority (blocks, km/hr)
        temp_train.authority = 3
        temp_train.command_speed = 55

        # Add blocks to train object
        if line == Line.LINE_GREEN:
            if block_to in self.green_blocks_inter:
                temp_train.route_switches_arr = copy.deepcopy(self.green_route_switches)
                temp_train.route_blocks_arr = copy.deepcopy(self.green_route_blocks)

                temp_train.route_blocks_arr.pop()
                temp_train.route_blocks_arr.extend(self.green_blocks_inter)
                temp_train.route_blocks_arr.extend(self.green_route_blocks_multiple)
                temp_train.route_blocks_arr.append(-1)

                temp_train.route_switches_arr.pop()
                temp_train.route_switches_arr.append(1)
                temp_train.route_switches_arr.extend(self.green_route_switches_inter)
                temp_train.route_switches_arr.pop()
                temp_train.route_switches_arr.append(0)
            else:
                temp_train.route_switches_arr = self.green_route_switches
                temp_train.route_blocks_arr = self.green_route_blocks

        else:
            if block_to in self.red_blocks_inter:
                temp_train.route_switches_arr = copy.deepcopy(self.red_route_switches)
                temp_train.route_blocks_arr = copy.deepcopy(self.red_route_blocks)

                temp_train.route_blocks_arr.pop()
                temp_train.route_blocks_arr.extend(self.red_blocks_inter)
                temp_train.route_blocks_arr.extend(self.red_route_blocks_multiple)
                temp_train.route_blocks_arr.append(-1)

                temp_train.route_switches_arr.pop()
                temp_train.route_switches_arr.extend(self.red_route_switches_inter)
                temp_train.route_switches_arr.pop()
                temp_train.route_switches_arr.append(0)
            else:
                temp_train.route_switches_arr = self.red_route_switches
                temp_train.route_blocks_arr = self.red_route_blocks

        #print(list(map(bool, temp_train.route_switches_arr)))
        #print(temp_train.route_blocks_arr)

        # Add train to this array
        self.trains_arr.append(temp_train)
        self.train_numbers.append(self.next_train_num)

        # Send signal to Track Controller
        signals.swtrack_dispatch_train.emit(temp_train.train_id,
                                            temp_train.destination_block,
                                            temp_train.command_speed,
                                            temp_train.authority,
                                            temp_train.line_on,
                                            list(map(bool, temp_train.route_switches_arr)))

        # Increment the next train number counter
        self.next_train_num += 1

    def return_occupancies(self, line):
        """ Function which returns an array of track occupancies for CTCUI to show """

        to_send = []
        if line == Line.LINE_GREEN:
            for i in range(len(self.blocks_green_arr)):
                to_send.append(self.blocks_green_arr[i].occupied)
        elif line == Line.LINE_RED:
            for i in range(len(self.blocks_red_arr)):
                to_send.append(self.blocks_red_arr[i].occupied)
        else:
            raise Exception('CTC : TrainSystem.return_occupancies recieved an erronious input')
        return to_send

    def return_closures(self, line):
        """ Function which returns an array of track closures for CTCUI to show """

        to_send = []
        if line == Line.LINE_GREEN:
            for i in range(len(self.blocks_green_arr)):
                to_send.append(self.blocks_green_arr[i].open)
        elif line == Line.LINE_RED:
            for i in range(len(self.blocks_red_arr)):
                to_send.append(self.blocks_red_arr[i].open)
        else:
            raise Exception('CTC : TrainSystem.return_closures recieved an erronious input')
        return to_send

    def return_switch_positions(self, line):
        """ Function which returns an array of switches which CTCUI can show """

        to_send = []
        if line == Line.LINE_GREEN:
            for i in range(len(self.switches_green_arr)):
                to_send.append(self.switches_green_arr[i].track_switch_to_string())
        elif line == Line.LINE_RED:
            for i in range(len(self.switches_red_arr)):
                to_send.append(self.switches_red_arr[i].track_switch_to_string())
        else:
            raise Exception('CTC : TrainSystem.return_switch_positions recieved an erronious input')
        return to_send

    def update_blocks(self, ln, block, occ):
        """ Function which updates occupancies from Track Controller """

        if ln == Line.LINE_GREEN:
            if (block < 1) or (block > 150):
                raise Exception('TrainSystem : update_blocks received blocks out of\
                                 range for Green Line')
            else:
                self.blocks_green_arr[block - 1].occupied = occ
        else:
            if (block < 1) or (block > 76):
                raise Exception('TrainSystem : update_blocks received blocks out of\
                                 range for Red Line')
            else:
                self.blocks_green_arr[block - 1].occupied = occ

        # Update the location of the train with every block moved
        self.update_train_loc()

    def update_g_switches(self, sw_arr):
        """ Function which updates occupancies on green route """
        if len(sw_arr) != 6:
            raise Exception('CTC Recived Erronious Green Switch Array')
        for i in range(len(sw_arr)):
            self.switches_green_arr[i].occupied = sw_arr[i]

    def update_r_switches(self, sw_arr):
        """ Function which updates occupancies on red route """
        if len(sw_arr) != 7:
            raise Exception('CTC Recived Erronious Red Switch Array')
        for i in range(len(sw_arr)):
            self.switches_red_arr[i].occupied = sw_arr[i]

    def update_throughput(self, thr):
        """ Function which updates throughput of system """
        self.throughput = thr

    def update_train_loc(self):
        """ Function which updates location of a train on the green line """
        trains_on_green = []    # Keep running list of blocks a train is on
        trains_on_red = []

        for i in range(len(self.trains_arr)):
            if self.trains_arr[i].line_on == Line.LINE_GREEN:

                # If train has not made it out of the yard yet
                if self.trains_arr[i].index_on_route == 0:
                    if self.trains_arr[i].route_blocks_arr[1] not in trains_on_green:
                        if self.blocks_green_arr[self.trains_arr[i].route_blocks_arr[1] - 1]\
                        .occupied:
                            self.trains_arr[i].index_on_route += 1
                            trains_on_green.append(self.trains_arr[i].route_blocks_arr[1])
                        else:
                            continue
                # If train has reached the yard
                elif self.trains_arr[i].index_on_route == len(self.trains_arr[i].route_blocks_arr\
                - 1):
                    self.trains_arr.pop(i)
                    self.train_numbers.pop(i)
                    i -= 1
                # If train is already on tracks; Advance train if block it says its on is
                # not occupied
                else:
                    if not self.blocks_green_arr[self.trains_arr[i].route_blocks_arr\
                    [self.trains_arr[i].index_on_route] - 1].occupied:

                        self.trains_arr[i].index_on_route += 1

                        if self.trains_arr[i].authority == 1:
                            self.trains_arr[i].authority = 3
                        else:
                            self.trains_arr[i].authority -= 1

                        if self.trains_arr[i].command_speed == 55:
                            self.trains_arr[i].command_speed = 54
                        else:
                            self.trains_arr[i].command_speed = 55

                        # Send upated command speed and authority to SW Track Controller
                        signals.swtrack_update_authority.emit(self.trains_arr[i].train_id,\
                            self.trains_arr[i].authority)
                        signals.swtrack_update_speed.emit(self.trains_arr[i].train_id,\
                            self.trains_arr[i].command_speed)
                        trains_on_green.append(self.trains_arr[i].route_blocks_arr\
                            [self.trains_arr[i].index_on_route])
                    else:
                        continue

            # If Line on RED
            else:
                # If train has not made it out of the yard yet
                if self.trains_arr[i].index_on_route == 0:
                    if self.trains_arr[i].route_blocks_arr[1] not in trains_on_red:
                        if self.blocks_red_arr[self.trains_arr[i].route_blocks_arr[1] - 1]\
                        .occupied:
                            self.trains_arr[i].index_on_route += 1
                            trains_on_red.append(self.trains_arr[i].route_blocks_arr[1])
                        else:
                            continue
                # If train has reached the yard
                elif self.trains_arr[i].index_on_route == len(self.trains_arr[i].route_blocks_arr\
                - 1):
                    self.trains_arr.pop(i)
                    self.train_numbers.pop(i)
                    i -= 1
                # If train is already on tracks; Advance train if block it says its on is
                # not occupied
                else:
                    if not self.blocks_red_arr[self.trains_arr[i].route_blocks_arr\
                    [self.trains_arr[i].index_on_route] - 1].occupied:

                        self.trains_arr[i].index_on_route += 1

                        if self.trains_arr[i].authority == 1:
                            self.trains_arr[i].authority = 3
                        else:
                            self.trains_arr[i].authority -= 1

                        if self.trains_arr[i].command_speed == 55:
                            self.trains_arr[i].command_speed = 54
                        else:
                            self.trains_arr[i].command_speed = 55

                        # Send upated command speed and authority to SW Track Controller
                        signals.swtrack_update_authority.emit(self.trains_arr[i].train_id,\
                            self.trains_arr[i].authority)
                        signals.swtrack_update_speed.emit(self.trains_arr[i].train_id,\
                            self.trains_arr[i].command_speed)
                        trains_on_red.append(self.trains_arr[i].route_blocks_arr\
                            [self.trains_arr[i].index_on_route])
                    else:
                        continue

# Define a TrainSystem object to use; acts as equivalent of singleton class
ctc = TrainSystem()
