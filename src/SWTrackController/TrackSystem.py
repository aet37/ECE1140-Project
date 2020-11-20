from src.common_def import *
from src.SWTrackController.TrackControllerdef import *

class TrackSystem:
    def __init__(self):


        self.controller0blocks = [0, 62,61,60,59] #a
		self.controller1blocks = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76] #b
		self.controller2blocks = [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 101] #c
		self.controller3blocks = [77, 78, 79, 80, 81, 82, 83, 84] #d
		self.controller4blocks = [85, 78, 79, 80, 81, 82, 83, 84] #e
		self.controller5blocks = [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100] #f
		self.controller6blocks = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
		self.controller7blocks = [29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14] #h
		self.controller8blocks = [28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13] #i
		self.controller9blocks = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1] #j
		self.controller10blocks = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
		self.controller11blocks = [58, 59, 60, 61] #l


		self.controller12blocks = [1, 2, 3, 4, 5, 6, 7, 8, 9] #m
		self.controller13blocks = [0, 9, 10, 11, 12, 13, 14, 15] #n
		self.controller14blocks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] #o
		self.controller15blocks = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26] #p
		self.controller16blocks = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27] #q
		self.controller17blocks = [72, 73, 74, 75, 76, 27, 28, 29, 30, 31, 32] #r
		self.controller18blocks = [72, 73, 74, 75, 76, 28, 29, 30, 31, 32, 33] #s
		self.controller19blocks = [33, 34, 35, 36, 37] #t
		self.controller20blocks = [34, 35, 36, 37, 38] #u
		self.controller21blocks = [38, 39, 40, 41, 42, 43, 71, 70, 69, 68, 67] #v
		self.controller22blocks = [39, 40, 41, 42, 43, 44, 71, 70, 69, 68, 67] #w
		self.controller23blocks = [44, 45, 46, 47, 48, 49, 50, 51] #x
		self.controller24blocks = [45, 46, 47, 48, 49, 50, 51, 52] #y
		self.controller25blocks = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66] #z
        self.blocksControlled = [controller0blocks, controller1blocks, controller2blocks, controller3blocks, controller4blocks, controller5blocks, controller6blocks, controller7blocks, controller8blocks, controller9blocks, controller10blocks, controller11blocks, controller12blocks, controller13blocks, controller14blocks, controller15blocks, controller16blocks, controller17blocks, controller18blocks, controller19blocks, controller20blocks, controller21blocks, controller22blocks, controller23blocks, controller24blocks, controller25blocks]

        controller0 = TrackController(0,5)
        controller1 = TrackController(1,15)
        controller2 = TrackController(2,16)
        controller3 = TrackController(3,8)
        controller4 = TrackController(4,8)
        controller5 = TrackController(5,16)
        controller6 = TrackController(6,80)
        controller7 = TrackController(7,16)
        controller8 = TrackController(8,16)
        controller9 = TrackController(9,13)
        controller10 = TrackController(10,29)
        controller11 = TrackController(11,4)
        controller12 = TrackController(12,9)
        controller13 = TrackController(13,8)
        controller14 = TrackController(14,16)
        controller15 = TrackController(15,11)
        controller16 = TrackController(16,11)
        controller17 = TrackController(17,11)
        controller18 = TrackController(18,11)
        controller19 = TrackController(19,5)
        controller20 = TrackController(20,5)
        controller21 = TrackController(21,11)
        controller22 = TrackController(22,11)
        controller23 = TrackController(23,8)
        controller24 = TrackController(24,8)
        controller25 = TrackController(25,15)

        self.TrackController_arr = [controller0, controller1, controller2, controller3, controller4, controller5, controller6, controller7, controller8, controller9, controller10, controller11, controller12, controller13, controller14, controller15, controller16, controller17, controller18, controller19, controller20, controller21, controller22, controller23, controller24, controller25]


