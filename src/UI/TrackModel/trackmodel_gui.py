import os
import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QLabel, QComboBox
import sys
from PyQt5.QtCore import QTimer
#from src.UI.server_functions import *
#from src.UI.window_manager import window_list
import pyexcel
import pyexcel_io
import json
sys.path.insert(0, "C:\\Users\\Evan\\OneDrive\\Documents\\GitHub\\ECE1140-Project\\src\\TrackModel")
import TrackModelDef
trackList = []
greenSwitchNumber = 0
redSwitchNumber = 0


class TrackModelUi(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        # self.track1_info_timer = QTimer()
        # self.track1_info_timer.timeout.connect(self.update_times)

        uic.loadUi('src/UI/TrackModel/Map_Page.ui', self)

        self.show()
        global combo1
        combo1 = QComboBox()
        global combo2 
        combo2 = QComboBox()

        self.initUI()
        #self.stacked_widget.currentChanged.connect(self.set_button_state)
        #self.stacked_widget.setCurrentIndex(0)
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.check_current_block)
        self.update_timer.start(2000)

        self.show()
    def initUI(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        #self.button.clicked.connect(self.trainMenu1)
        addTrackButton = self.findChild(QtWidgets.QPushButton, 'add_track_button')
        addTrackButton.clicked.connect(self.readInData)

        logoutButton = self.findChild(QtWidgets.QPushButton, 'logout_button')
        logoutButton.clicked.connect(self.logout)

    # def update_times(self):
        # TODO get position string from Train Model in ??? UNITS
        # position_string = send_message(RequestCode.GET_POSITION_FROM_TRAINM)

        # convert position string to an int
        # int position = std::stoi(position_string)


        # send_message(RequestCode.GET_POSITION_FROM_TRAINM)


        #responsecode, speed = send_message(RequestCode.GET)
        #responsecode, block = send_message(RequestCode.GET_SIGNAL_TIMES)
        #if responsecode == ResponseCode.SUCCESS:
            #block = times.split(" ")
        # self.signal_1.setText('Currently on\nblock:\n NA')
        # self.signal_2.setText('Currently on\nblock:\n NA')
        # self.signal_3.setText('Currently on\nblock:\n NA')
        # self.signal_4.setText('Currently on\nblock:\n NA')
        # self.signal_5.setText('Currently on\nblock:\n NA')
        # self.signal_6.setText('Currently on\nblock:\n NA')
        # self.signal_7.setText('Currently on\nblock:\n NA')
        # self.signal_8.setText('Currently on\nblock:\n NA')
        # self.signal_9.setText('Currently on\nblock:\n NA')
        # self.signal_10.setText('Currently on\nblock:\n NA')
        # self.signal_11.setText('Currently on\nblock:\n NA')
        # self.signal_12.setText('Currently on\nblock:\n NA')
        # self.signal_13.setText('Currently on\nblock:\n NA')
        # self.signal_14.setText('Currently on\nblock:\n NA')
        # self.signal_15.setText('Currently on\nblock:\n NA')
        #else:
            #print(responsecode)
        # responsecode, switch = send_message(RequestCode.GET_SWITCH_POSITION)
        # if responsecode == ResponseCode.SUCCESS:
        #     switch = switch.split(" ")
        #     self.switch_5.setText('Switch flipped to:\n\n'+switch[0])
        # else:
        #     self.stopAllTimers()
        #     print('The server is not running')

        # send_message(RequestCode.SET_SPEED_LIMIT, self.speed_limit_1.text()[46:48])

        # responsecode, speed = send_message(RequestCode.GET_SPEED_LIMIT)
        # if responsecode == ResponseCode.SUCCESS:
        #     print(speed)
        # else:
        #     print('fail')
    def readInData(self):
        global greenSwitchNumber
        global redSwitchNumber
        dialog = QtWidgets.QFileDialog(self)
        fileInfo = dialog.getOpenFileName(self)
        
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

                newTrack = TrackModelDef.Track(trackInfo['Track'], trackInfo['Total Blocks'], trackInfo['tNumber'])
                trackList.append(newTrack)

                theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
                line = records.column['Line'][1]
                #combo1.addItem("Select "+line+" Line block")
                if (line == "Green"):
                    theTabWidget.addTab(combo1, line+" Line")
                    theCombo = combo1
                    trackNumber = 0
                elif (line == "Red"):
                    theTabWidget.addTab(combo2, line+" Line")
                    theCombo = combo2
                    trackNumber = 1


                for x in range(records.number_of_rows()):
                    blockInfo = {}
                    blockNumber = records.column['Block Number'][x]
                    theCombo.addItem("Block "+str(blockNumber)) 

                    blockLength = records.column['Block Length (m)'][x]
                    blockGrade = records.column['Block Grade (%)'][x]
                    blockSpeedLimit = records.column['Speed Limit (Km/Hr)'][x]
                    #blockStation = blockStation
                    #blockSwitch = destinationSwitchList
                    blockElevation = records.column['Elevation (m)'][x]
                    blockCumulativeElevation = round(records.column['Cumulative Elevation (m)'][x], 2)
                    blockDirection = records.column['Direction'][x]
                    blockSection = records.column['Section'][x]
                    blockInfo['Track'] = trackNumber
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

                    theBlock = TrackModelDef.Block(blockNumber, blockLength, blockGrade, blockSpeedLimit,
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



                    #jsonString = json.dumps(blockInfo)
                    #print(jsonString)
                    #send_message(RequestCode.TRACK_MODEL_GUI_BLOCK, str(jsonString))

                self.switch_block()

            else:
                print('error')
    def check_current_block(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        if (theTabWidget.tabText(theTabWidget.currentIndex()) == "Green"):
            combo1.currentIndexChanged.connect(self.switch_block)
        elif (theTabWidget.tabText(theTabWidget.currentIndex()) == "Red"):
            combo1.currentIndexChanged.connect(self.switch_block)
            combo2.currentIndexChanged.connect(self.switch_block)
    
    def getTrack(self, trackColor):
        for x in trackList:
            if (x.lineName == trackColor):
                return x
        return ""


    def switch_block(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        theIndex = theTabWidget.currentIndex()
        theLine = theTabWidget.tabText(theIndex)
        theLine = theLine.replace(" Line", "")

        if (self.getTrack(theLine) != ""):
            theTrack = self.getTrack(theLine)
            
            line_name_label = self.findChild(QtWidgets.QLabel, 'line_name_label')
            line_name_label.setText(theLine + " Line")

            if (theLine == "Green"):
                currentComboBlock = str(combo1.currentText())
            else:
                currentComboBlock = str(combo2.currentText())
            
            currentComboBlock = currentComboBlock[6:]

            block_number_label = self.findChild(QtWidgets.QLabel, 'block_number_label')
            block_number_label.setText("Block " + currentComboBlock)

            theBlock = theTrack.getBlock(int(currentComboBlock))

            section_label = self.findChild(QtWidgets.QLabel, 'section_label')
            section_label.setText("Section: " + str(theBlock.blockSection))

            elevation_label = self.findChild(QtWidgets.QLabel, 'elevation_label')
            elevation_label.setText("Elevation\n\n"+ str(theBlock.blockElevation) + " m")

            cumulative_elevation_label = self.findChild(QtWidgets.QLabel, 'cumulative_elevation_label')
            cumulative_elevation_label.setText("Cumulative Elevation\n\n"+ str(theBlock.blockCumulativeElevation)+ " m")

            length_label = self.findChild(QtWidgets.QLabel, 'length_label')
            length_label.setText("Block Length:\n\n"+ str(theBlock.blockLength)+ " m")

            grade_label = self.findChild(QtWidgets.QLabel, 'grade_label')
            grade_label.setText("Block Grade:\n\n"+ str(theBlock.blockGrade)+'%')

            speed_limit_label = self.findChild(QtWidgets.QLabel, 'speed_limit_label')
            speed_limit_label.setText("Speed Limit:\n\n"+ str(theBlock.blockSpeedLimit)+" Km/Hr")

            underground_label = self.findChild(QtWidgets.QLabel, 'underground_label')
            underground_label.setText("Underground:\n\n"+ str(theBlock.blockUnderground))

            station_name_label = self.findChild(QtWidgets.QLabel, 'station_name_label')
            station_name_label.setText("Station Name:\n\n"+ theBlock.getStationName())

            tickets_sold_label = self.findChild(QtWidgets.QLabel, 'tickets_sold_label')
            tickets_sold_label.setText("Tickets Sold:\n\n"+ str(theBlock.getTicketsSold()))

            passengers_boarded_label = self.findChild(QtWidgets.QLabel, 'passengers_boarded_label')
            passengers_boarded_label.setText("Passengers Boarded:\n\n"+ str(theBlock.getPassengersBoarded()))

            passengers_exited_label = self.findChild(QtWidgets.QLabel, 'passengers_exited_label')
            passengers_exited_label.setText("Passengers Exited:\n\n"+ str(theBlock.getPassengersExited()))

            exit_side_label = self.findChild(QtWidgets.QLabel, 'exit_side_label')
            exit_side_label.setText("Exit Side:\n\n"+ theBlock.getExitSide())

            occupied_label = self.findChild(QtWidgets.QLabel, 'occupied_label')
            occupancy = theBlock.blockOccupied
            if (occupancy == -1):
                occupied_label.setText("Occupied by:\n\nNone")
            else:
                occupied_label.setText("Occupied by:\n\n"+ str(occupancy))

            switch_list_label = self.findChild(QtWidgets.QLabel, 'switch_list_label')
            switch_list_label.setText("Switches possible:\n\n" + theBlock.getSwitchBlocksString())

            current_switch_label = self.findChild(QtWidgets.QLabel, 'current_switch_label')
            current_switch_label.setText("Switch flipped to:\n\n" + theBlock.getSwitchCurrentString())

            track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
            trackHeater = theTrack.trackHeater
            if (trackHeater):
                track_heater_button.setText("On")
                track_heater_button.setStyleSheet("background-color : green")
            else:
                track_heater_button.setText("Off")
                track_heater_button.setStyleSheet("background-color : red")

            failure_mode_label = self.findChild(QtWidgets.QLabel, 'failure_mode_label')
            failure = theBlock.failureMode
            if (failure == 0):
                failure_mode_label.setText("Failure Mode:\n\n"+ "No Failures")
            elif (failure == 1):
                failure_mode_label.setText("Failure Mode:\n\n"+ "Power Failure")
            elif (failure == 2):
                failure_mode_label.setText("Failure Mode:\n\n"+ "Broken Track")
            elif (failure == 3):
                failure_mode_label.setText("Failure Mode:\n\n"+ "Track Circuit Failure")


    def trackInfo1(self):
        self.stopAllTimers()
        self.track1_info_timer.start(1000)

    def stopAllTimers(self):
        self.track1_info_timer.stop()

    def logout(self):
        """Removes this window from the list"""
        window_list.remove(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrackModelUi()
    app.exec_()
