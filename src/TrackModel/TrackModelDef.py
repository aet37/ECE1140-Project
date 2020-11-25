"""
    @file TrackModelDef.py

    @brief Declaration of Structs and Enums used in Track Model

    @author Evan Kutney

    @date 11.18.2020
"""
import sys
sys.path.append(".")
#sys.path.insert(0, "C:\\Users\\Evan\\OneDrive\\Documents\\GitHub\\ECE1140-Project\\src")
from src.common_def import *

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
        return self.blockList[blockNumber - 1]

    def addBlock(self, theBlock):
        self.blockList.append(theBlock)

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
        self.failureMode = 0

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
        if (switch == False):
            self.currentSwitch = self.block1
        else:
            self.currentSwitch = self.block2


class SignalHandler:
    """"""
    def __init__(self):
        signals.trackmodel_dispatch_train.connect(self.dispatchTrain)
        signals.trackmodel_update_occupancy.connect(self.updateOccupancy)

    def updateOccupancy(self, trainId, line, blockId, trainOrNot):
        if (line == Line.LINE_GREEN):
            theTrack = getTrack("Green")
            theBlock = theTrack.getBlock(blockId)
            if (trainOrNot == 0):
                theBlock.updateOccupancy(trainId)
            else:
                theBlock.updateOccupancy(-1)
        else:
            theTrack = TrackModelDef.getTrack("Red")
            theBlock = theTrack.getBlock(blockId)
            if (trainOrNot == 0):
                theBlock.updateOccupancy(trainId)
            else:
                theBlock.updateOccupancy(-1)

        # Tell swtrack the occupancy
        signals.swtrack_update_occupancies.emit(blockId, line, trainOrNot)

    def dispatchTrain(self, trainId, destinationBlock, commandSpeed, authority, currentLine, switch_arr):
        logger.critical("Received trackmodel_dispatch_train")
        logger.critical(trackList)
        logger.critical(currentLine)
        if (currentLine == Line.LINE_GREEN):
            theTrack = getTrack("Green")
            for i in green_route_blocks:
                theBlock = theTrack.getBlock(i)
                signals.train_model_receive_block.emit(0, i, theBlock.blockElevation, theBlock.blockGrade, theBlock.blockLength, theBlock.blockSpeedLimit, theBlock.blockDirection)
        else:
            theTrack = getTrack("Red")
            for i in red_route_blocks:
                theBlock = theTrack.getBlock(i)
                signals.train_model_receive_block.emit(1, i, theBlock.blockElevation, theBlock.blockGrade, theBlock.blockLength, theBlock.blockSpeedLimit, theBlock.blockDirection)

        signals.train_model_dispatch_train.emit(trainId, destinationBlock, commandSpeed, authority, currentLine)

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
                        stationName = records.column['Stations'][x]
                        stationExitSide = records.column['Exit Side'][x]
                        theBlock.addStation(stationName, stationExitSide)

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


                    newTrack.addBlock(theBlock)
                    signals.train_model_recieve_block.emit(trackInfo['tNumber'], blockNumber - 1, blockElevation, blockSlope, blockLength, blockSpeedLimit, blockDirection)



                    #jsonString = json.dumps(blockInfo)
                    #print(jsonString)
                    #send_message(RequestCode.TRACK_MODEL_GUI_BLOCK, str(jsonString))

                self.switch_block()

            else:
                print('error')


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