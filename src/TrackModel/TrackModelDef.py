"""
    @file TrackModelDef.py

    @brief Declaration of Structs and Enums used in Track Model

    @author Evan Kutney

    @date 11.18.2020
"""
from src.common_def import *
import sys
sys.path.append(".")
from src.signals import signals
from src.logger import get_logger
#from src.UI.TrackModel import trackmodel_gui
import random
import pyexcel
import pyexcel_io
from traceback import print_stack
from src.timekeeper import timekeeper



logger = get_logger(__name__)

greenSwitchNumber = 0
redSwitchNumber = 0
environmentalTemp = 70
trackList = []

red_route_blocks = [9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75,
		            74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51,
		            52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46,
		            45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,
		            23, 22, 21, 20, 19, 18, 17, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9]

red_route_double_blocks = [9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75,
		                        74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51,
		                        52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46,
		                        45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,
		                        23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 
                                17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75, 74, 73, 72, 33, 34, 35, 36, 37, 38,
                                71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                                61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37,
                                36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,23, 22, 21, 20, 19, 18, 17, 16, 1, 2,
                                3, 4, 5, 6, 7, 8, 9]


green_route_blocks = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
		                           82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84,
		                           83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
		                           112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
		                           129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145,
		                           146, 147, 148, 149, 150, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15,
		                           14, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
		                           22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
		                           43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]

# green_route_blocks_with_direction = [[62, 0], [63, 0], [64, 0], [65, 0], [66, 0], [67, 0], [68, 0], [69, 0], [70, 0], [71, 0], 
# [72, 0], [73, 0], [74, 0], [75, 0], [76, 0], [77, 0], [78, 0], [79, 0], [80, 0], [81, 0], [82, 0], [83, 0], [84, 0], [85, 0], 
# [86, 0], [87, 0], [88, 0], [89, 0], [90,0], [91, 0], [92, 0], [93, 0], [94, 0], [95, 0], [96, 0], [97, 0], [98, 0], [99, 0], 
# [100, 0], [85, 1], [84, 1], [83, 1], [82, 1], [81, 1], [80, 1], [79, 1], [78, 1], [77, 1], [101, 0], [102, 0], [103, 0],
# [104, 0], [105, 0], [106, 0], [107, 0], [108, 0], [109, 0], [110, 0], [111, 0], [112, 0], [113, 0], [114, 0], [115, 0],
# [116, 0], [117, 0], [118, 0], [119, 0], [120, 0], [121, 0], [122, 0], [123, 0], [124, 0], [125, 0], [126, 0], [127, 0],
# [128, 0], [129, 0], [130, 0], [131, 0], [132, 0], [133, 0], [134, 0], [135, 0], [136, 0], [137, 0], [138, 0], [139, 0],
# [140, 0], [141, 0], [142, 0], [143, 0], [144, 0], [145, 0], [146, 0], [147, 0], [148, 0], [149, 0], [150, 0], [29, 0],
# [28, 0], [27, 0], [26, 0], [25, 0], [24, 0], [23, 0], [22, 0], [21, 0], [20, 0], [19, 0], [18, 0], [17, 0], [16, 0],
# [15, 0], [14, 0], [13, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], 
# [12, 0], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1], 
# [25, 1], [26, 1], [27, 1], [28, 1], [29, 1], [30, 0], [31, 0], [32, 0], [33, 0], [34, 0], [35, 0], [36, 0], [37, 0],
#  [38, 0], [39, 0], [40,  0], [41, 0], [42, 0], [43, 0], [44, 0], [45, 0], [46, 0], [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
"""
	@struct Track

	@brief Structure that holds data about a Track
"""
class Track:
    def __init__(self, line, totalBlocks, trackNumber):
        self.lineName = line
        self.totalBlocks = totalBlocks
        self.trackNumber = trackNumber
        self.trackHeater = False
        self.switchList = [] # switchList.append(Switch(blah, blah))
        self.stationList = []
        self.blockList = []

    def getBlock(self, blockNumber):
        #logger.critical("BlockNumber = " + str(blockNumber))
        #print_stack()
        return self.blockList[blockNumber - 1]

    def addBlock(self, theBlock):
        self.blockList.append(theBlock)

    def setTrackHeater(self, heaterBool):
        self.trackHeater = heaterBool
    
    def getStationBlocks(self, stationName):
        for x in self.stationList:
            if (x.stationName == stationName):
                return x.blockList
        return 0

class Block:
    def __init__(self, blockNumber, blockLength, blockGrade, blockSpeedLimit,
    blockElevation, blockCumulativeElevation, blockDirection, blockUnderground,
    blockSection, blockRailwayCrossing):
        self.blockNumber = blockNumber
        self.blockLength = blockLength
        self.blockGrade = blockGrade
        self.blockSpeedLimit = blockSpeedLimit
        self.blockElevation = blockElevation
        self.blockCumulativeElevation = blockCumulativeElevation
        self.blockDirection = blockDirection
        self.blockUnderground = blockUnderground
        self.blockSection = blockSection
        self.blockRailwayCrossing = blockRailwayCrossing
        self.blockStation = None
        self.blockSwitch = None
        self.blockOccupied = -1
        self.brokenRailFailure = False
        self.powerFailure = False
        self.trackCircuitFailure = False

    def addStation(self, stationName, stationExitSide):
        self.blockStation = Station(stationName, stationExitSide)

    def addSwitch(self, switchNumber, block1, block2):
        self.blockSwitch = Switch(switchNumber, block1, block2)

    def updateOccupancy(self, occupancy):
        self.blockOccupied = occupancy

    def getStationName(self):
        if (self.blockStation == None):
            return "NA"
        else:
            return self.blockStation.stationName

    def getTicketsSold(self):
        if (self.blockStation == None):
            return 0
        else:
            return self.blockStation.ticketsSold

    def getPassengersBoarded(self):
        if (self.blockStation == None):
            return 0
        else:
            return self.blockStation.passengersBoarded

    def getPassengersExited(self):
        if (self.blockStation == None):
            return 0
        else:
            return self.blockStation.passengersExited

    def getExitSide(self):
        if (self.blockStation == None):
            return "NA"
        else:
            return self.blockStation.stationExitSide

    def getSwitchBlocksString(self):
        if (self.blockSwitch == None):
            return "NA"
        else:
            return str(self.blockSwitch.block1) + ", " + str(self.blockSwitch.block2)

    def getSwitchCurrentString(self):
        if (self.blockSwitch == None):
            return "NA"
        else:
            return str(self.blockSwitch.currentSwitch)

"""
	@struct Station

	@brief Structure that holds data about a Station
"""
class Station:
    def __init__(self, stationName, stationExitSide):
        self.stationName = stationName
        self.stationExitSide = stationExitSide
        self.ticketsSold = 0
        self.passengersBoarded = 0
        self.passengersExited = 0
        self.blockList = []

    def updateTicketsSold(self, ticketsSold):
        self.ticketsSold = ticketsSold

    def updatePassengersBoarded(self, passengersBoarded):
        self.passengersBoarded = passengersBoarded

    def updatePassengersExited(self, passengersExited):
        self.passengersExited = passengersExited
"""
	@struct Switch

	@brief Structure that holds data about a Switch

	@note -1 denotes yard
"""
class Switch:
    def __init__(self, switchNumber, block1, block2):
        self.switchNumber = switchNumber
        if (block1 > block2):
            block3 = block1
            block1 = block2
            block2 = block3

        self.block1 = block1
        self.block2 = block2
        self.currentSwitch = self.block1

    def setSwitch(self, switch):
        if (switch):
            self.currentSwitch = self.block1
        else:
            self.currentSwitch = self.block2

class SignalHandler:
    """"""
    def __init__(self):
        signals.trackmodel_dispatch_train.connect(self.dispatchTrain)
        signals.trackmodel_update_occupancy.connect(self.updateOccupancy)
        signals.trackmodel_update_command_speed.connect(self.updateCommandSpeed)
        signals.trackmodel_update_authority.connect(self.updateAuthority)
        signals.trackmodel_update_switch_positions.connect(self.updateSwitchPositions)
        signals.trackmodel_update_tickets_sold.connect(self.updateTicketsSold)
        signals.trackmodel_update_passengers_exited.connect(self.updatePassengersExited)

    def updatePassengersExited(self, line, trainId, blockNumber, passengersExited, spaceOnTrain, totalSeats):
        if (line == Line.LINE_GREEN):
            theTrack = getTrack("Green")
        else:
            theTrack = getTrack("Red")
        
        theBlock = theTrack.getBlock(blockNumber)
        theStation = theBlock.blockStation
    
        blockList = theTrack.getStationBlocks(theStation.stationName)

        for x in blockList:
            theTrack.getBlock(x).blockStation.passengersExited += passengersExited

        passengersLeftToBoard = theStation.ticketsSold - theStation.passengersBoarded
        
        if (passengersLeftToBoard > spaceOnTrain):
            for y in blockList:
                theTrack.getBlock(y).blockStation.passengersBoarded += spaceOnTrain
            totalPassengers = totalSeats
            signals.train_model_update_passengers.emit(trainId, totalPassengers)
        else:
            for z in blockList:
                theTrack.getBlock(z).blockStation.passengersBoarded += passengersLeftToBoard
            totalPassengers = totalSeats - (spaceOnTrain - passengersLeftToBoard)
            signals.train_model_update_passengers.emit(trainId, totalPassengers)

    def updateSwitchPositions(self, line, number, position):
        if (line == Line.LINE_GREEN):
            theLine = getTrack("Green")
        else:
            theLine = getTrack("Red")
        theLine.getBlock(theLine.switchList[number]).blockSwitch.setSwitch(position)
        signals.trackmodel_update_gui.emit()

    def updateTicketsSold(self):
        totalTickets = 0
        if (getTrack("Green") != None):
            theLine = getTrack("Green")
            for x in theLine.stationList:
                x.ticketsSold = random.randrange(30, 200, 1)
                totalTickets = totalTickets + x.ticketsSold
                for y in x.blockList:
                    theLine.getBlock(y).blockStation.ticketsSold = x.ticketsSold
                    theLine.getBlock(y).blockStation.passengersBoarded = 0
                    theLine.getBlock(y).blockStation.passengersExited = 0

        if (getTrack("Red") != None):
            theLine = getTrack("Red")
            for x in theLine.stationList:
                x.ticketsSold = random.randrange(30, 200, 1)
                totalTickets = totalTickets + x.ticketsSold
                x.passengersBoarded = 0
                x.passengersExited = 0
                for y in x.blockList:
                    theLine.getBlock(y).blockStation.ticketsSold = x.ticketsSold
                    theLine.getBlock(y).blockStation.passengersBoarded = 0
                    theLine.getBlock(y).blockStation.passengersExited = 0

        signals.update_throughput.emit(totalTickets)
        signals.trackmodel_update_gui.emit()


    def updateAuthority(self, line, blockNumber, newAuthority):
        if (line == Line.LINE_GREEN):
            theLine = getTrack("Green")
        else:
            theLine = getTrack("Red")
        
        theBlock = theLine.getBlock(blockNumber)

        trainId = theBlock.blockOccupied

        if (trainId == -1):
            assert False
        
        signals.train_model_update_authority.emit(trainId, newAuthority)

    # def updateAuthority(self, trainId, newAuthority):
    #     signals.train_model_update_authority.emit(trainId, newAuthority)

    def updateOccupancy(self, trainId, line, currentBlock, trainOrNot, trainDirection):
        if (line == Line.LINE_GREEN):
            theTrack = getTrack("Green")
            theBlock = theTrack.getBlock(currentBlock)
            if (currentBlock == 100):
                trainDirection = False
                signals.train_model_switch_direction.emit(trainId, trainDirection)

            elif (currentBlock == 77 and not trainDirection):
                trainDirection = True
                signals.train_model_switch_direction.emit(trainId, trainDirection)

            elif (currentBlock == 12 and trainDirection):
                trainDirection = False
                signals.train_model_switch_direction.emit(trainId, trainDirection)

            elif (currentBlock == 29 and not trainDirection):
                trainDirection = True
                signals.train_model_switch_direction.emit(trainId, trainDirection)

        else:
            theTrack = getTrack("Red")
            if (currentBlock == 66):
                trainDirection = False
                signals.train_model_switch_direction.emit(trainId, trainDirection)


        if (currentBlock != 0):
            theBlock = theTrack.getBlock(currentBlock)
            if (trainOrNot):
                theBlock.updateOccupancy(trainId)
                # if (theBlock.blockStation != None):
                #     for x in theTrack.stationList:
                #         if (x.stationName == theBlock.blockStation.stationName):
                #             for y in x.blockList:
                #                 theTrack.getBlock(y).blockStation.
            else:
                theBlock.updateOccupancy(-1)

        # Tell swtrack the occupancy
        signals.swtrack_update_occupancies.emit(trainId, line, currentBlock, trainOrNot)
        signals.trackmodel_update_gui.emit()

    def dispatchTrain(self, trainId, destinationBlock, commandSpeed, authority, currentLine, switch_arr):
        logger.debug("Received trackmodel_dispatch_train")
        if (currentLine == Line.LINE_GREEN):
            theTrack = getTrack("Green")
            route = green_route_blocks
            for i in green_route_blocks:
                theBlock = theTrack.getBlock(i)
                #print("Trackmodel block: " + str(theBlock.blockNumber) + " station: " + str(theBlock.blockStation != None))
                signals.train_model_receive_block.emit(0, i, theBlock.blockElevation, theBlock.blockGrade, theBlock.blockLength, theBlock.blockSpeedLimit, theBlock.blockDirection, theBlock.blockStation != None)
        else:
            theTrack = getTrack("Red")
            route = red_route_blocks
            for i in red_route_blocks:
                theBlock = theTrack.getBlock(i)
                signals.train_model_receive_block.emit(1, i, theBlock.blockElevation, theBlock.blockGrade, theBlock.blockLength, theBlock.blockSpeedLimit, theBlock.blockDirection, theBlock.blockStation != None)

        signals.train_model_dispatch_train.emit(trainId, destinationBlock, commandSpeed, authority, currentLine, route)

    # Examples of fileInfo inputs below
    #('C:/Users/Evan/OneDrive/Documents/GitHub/ECE1140-Project/resources/Green Line.xlsx', 'All Files (*)')
    #('C:/Users/Evan/OneDrive/Documents/GitHub/ECE1140-Project/resources/Red Line.xlsx', 'All Files (*)')
    def readInData(fileInfo):
        global greenSwitchNumber
        global redSwitchNumber

        testXlsx = fileInfo[0].split('.')
        if (testXlsx[1] != 'xlsx'):
            print('File type must be .xlsx, your file was of type: .'+testXlsx[1])
        else:
            #print(fileInfo[0])
            records = pyexcel.get_sheet(file_name=fileInfo[0])
            records.name_columns_by_row(0)
            #print (records.number_of_rows())
            # print(records.content)
            trackInfo = {}
            # stationList = []
            # switchList = []
            # trackInfo['Stations'] = stationList
            # trackInfo['Switches'] = switchList
            # trackInfo['Block List'] = ''
            # stations = 0;

            if (records.number_of_rows() > 0):
                # set Line inside trackInfo
                trackInfo['Track'] = records.column['Line'][1]

                if (records.column['Line'][1] == "Red"):
                    trackInfo['tNumber'] = 1
                else:
                    trackInfo['tNumber'] = 0

                # set totalBlocks inside trackInfo
                trackInfo['Total Blocks'] = records.number_of_rows()

                newTrack = Track(trackInfo['Track'], trackInfo['Total Blocks'], trackInfo['tNumber'])
                trackList.append(newTrack)

                line = records.column['Line'][1]

                #trackmodel_gui.TrackModelUi.addTab(self, line)
                #combo1.addItem("Select "+line+" Line block")

                for x in range(records.number_of_rows()):
                    blockInfo = {}
                    blockNumber = records.column['Block Number'][x]
                    #theCombo.addItem("Block "+str(blockNumber))

                    blockLength = records.column['Block Length (m)'][x]
                    blockGrade = records.column['Block Grade (%)'][x]
                    blockSpeedLimit = records.column['Speed Limit (Km/Hr)'][x]
                    #blockStation = blockStation
                    #blockSwitch = destinationSwitchList
                    blockElevation = records.column['Elevation (m)'][x]
                    blockCumulativeElevation = round(records.column['Cumulative Elevation (m)'][x], 2)
                    blockDirection = records.column['Direction'][x]
                    blockSection = records.column['Section'][x]
                    blockInfo['Track'] = len(trackList)
                    blockInfo['Number'] = blockNumber
                    blockInfo['Length'] = blockLength
                    blockInfo['Grade'] = blockGrade
                    blockInfo['Speed Limit'] = blockSpeedLimit
                    blockInfo['Elevation'] = blockElevation
                    blockInfo['Cumulative Elevation'] = blockCumulativeElevation
                    blockInfo['Direction'] = blockDirection


                    if (records.column['Underground'][x] != ""):
                        blockInfo['Underground'] = "true"
                        blockUnderground = True
                    else:
                        blockInfo['Underground'] = "false"
                        blockUnderground = False

                    blockInfo['Section'] = blockSection

                    if (records.column['Railway Crossing'][x] != ""):
                        blockInfo['Railway Crossing'] = "true"
                        blockRailwayCrossing = True
                    else:
                        blockInfo['RailwayCrossing'] = "false"
                        blockRailwayCrossing = False

                    theBlock = Block(blockNumber, blockLength, blockGrade, blockSpeedLimit,
                    blockElevation, blockCumulativeElevation, blockDirection, blockUnderground,
                    blockSection, blockRailwayCrossing)

                    if (records.column['Stations'][x] != ""):
                        stationBool = True
                        stationName = records.column['Stations'][x]
                        stationExitSide = records.column['Exit Side'][x]
                        theBlock.addStation(stationName, stationExitSide)
                        appended = False
                        theTrack = getTrack(trackInfo['Track'])
                        for y in theTrack.stationList:
                            if (y.stationName == stationName):
                                y.blockList.append(blockNumber)
                                appended = True
                        if (not appended):
                            theTrack.stationList.append(Station(stationName, stationExitSide))
                            theTrack.stationList[len(theTrack.stationList) - 1].blockList.append(blockNumber)
                    else:
                        stationBool = False

                    if (records.column['Switches'][x] != ""):
                        switchList = records.column['Switches'][x]
                        switchList = switchList.split(',')
                        if (line == "Green"):
                            greenSwitchNumber = greenSwitchNumber + 1
                            switchNumber = greenSwitchNumber
                        else:
                            redSwitchNumber = redSwitchNumber + 1
                            switchNumber = redSwitchNumber

                        block1 = int(switchList[0])
                        block2 = int(switchList[1])
                        theBlock.addSwitch(switchNumber, block1, block2)
                        theTrack.switchList.append(theBlock.blockNumber)

                    newTrack.addBlock(theBlock)

                    if (blockNumber == 1):
                        signals.train_model_receive_block.emit(trackInfo['tNumber'], 0, 0, 0, 10, blockSpeedLimit, blockDirection, stationBool)

                    signals.train_model_receive_block.emit(trackInfo['tNumber'], blockNumber, blockElevation, blockGrade, blockLength, blockSpeedLimit, blockDirection, stationBool)


                    #jsonString = json.dumps(blockInfo)
                    #print(jsonString)
                    #send_message(RequestCode.TRACK_MODEL_GUI_BLOCK, str(jsonString))

                # self.switch_block()

            else:
                print('error')

    def updateCommandSpeed(self, trainId, newSpeed):
        signals.train_model_update_command_speed.emit(trainId, newSpeed)

# "Green" or "Red"
def getTrack(trackColor):
    for x in trackList:
        if (x.lineName == trackColor):
            return x
    return None


signal_handler = SignalHandler()

# Do Not allow to be run as Main Module
if __name__ == "__main__":
	raise Exception("Not to be run as a module")
