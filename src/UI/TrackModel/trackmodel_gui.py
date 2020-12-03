import os
import sys
import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QLabel, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer
#from src.UI.server_functions import *
#from src.UI.window_manager import window_list
import json
import pyexcel
import pyexcel_io
import random
sys.path.append(".")
from src.TrackModel import TrackModelDef
from src.signals import *
from src.UI.window_manager import window_list
from src.logger import get_logger
logger = get_logger(__name__)


class TrackModelUi(QtWidgets.QMainWindow):
    global combo1
    global combo2
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

        global tabsAdded
        tabsAdded = 0

        self.initUI()

        self.show()

    def initUI(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        #self.button.clicked.connect(self.trainMenu1)
        addTrackButton = self.findChild(QtWidgets.QPushButton, 'add_track_button')
        addTrackButton.clicked.connect(self.getFileName)

        logoutButton = self.findChild(QtWidgets.QPushButton, 'logout_button')
        logoutButton.clicked.connect(self.logout)

        if (len(TrackModelDef.trackList) > 0):
            if (TrackModelDef.getTrack("Green") != None):
                self.addTab("Green", 150)
            if (TrackModelDef.getTrack("Red") != None):
                self.addTab("Red", 76)

        track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
        track_heater_button.clicked.connect(self.update_track_heater)

        broken_rail_failure_button = self.findChild(QtWidgets.QPushButton, 'broken_rail_failure_button')
        broken_rail_failure_button.clicked.connect(self.update_broken_rail_failure)

        power_failure_button = self.findChild(QtWidgets.QPushButton, 'power_failure_button')
        power_failure_button.clicked.connect(self.update_power_failure)

        track_circuit_failure_button = self.findChild(QtWidgets.QPushButton, 'track_circuit_failure_button')
        track_circuit_failure_button.clicked.connect(self.update_track_circuit_failure)

        set_random_temp_button = self.findChild(QtWidgets.QPushButton, 'set_random_temp_button')
        set_random_temp_button.clicked.connect(self.set_random_temperature)

        set_manual_temp_button = self.findChild(QtWidgets.QPushButton, 'set_manual_temp_button')
        set_manual_temp_button.clicked.connect(self.set_manual_temperature)

        signals.trackmodel_update_gui.connect(self.switch_block) # TODO: might need to make sure there is a track before trying to update 
        
        change_block_length_button = self.findChild(QtWidgets.QPushButton, 'change_block_length_button')
        change_block_length_button.clicked.connect(self.changeBlockLength)

    def changeBlockLength(self):
        length, bleh = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter a block length between 10 and 1000:')
        message = QMessageBox()
        
        length_label = self.findChild(QtWidgets.QLabel, 'length_label')
        try:
            length = float(length)
            if (length <= 1000 and length >= 10):
                length_label.setText("Block Length:\n\n"+ str()+ " m")
                theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
                theIndex = theTabWidget.currentIndex()
                theLine = theTabWidget.tabText(theIndex)
                theLine = theLine.replace(" Line", "")
                theTrack = TrackModelDef.getTrack(theLine)

                if (theLine == "Green"):
                    currentComboBlock = str(combo1.currentText())
                    line = Line.LINE_GREEN
                else:
                    currentComboBlock = str(combo2.currentText())
                    line = Line.LINE_RED

                currentComboBlock = int(currentComboBlock[6:])

                theBlock = theTrack.getBlock(currentComboBlock)
                theBlock.blockLength = length
                signals.train_model_edit_block.emit(line, int(currentComboBlock), length)
                signals.trackmodel_update_gui.emit()
            else:
                message.setText("Temperature outside of range!\nEnter a value between 10 and 1000, inclusive")
                message.exec_()
        except ValueError:
            message.setText("Invalid input: Not an integer")
            message.exec_()

    def set_manual_temperature(self):
        track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
        current_temperature_label = self.findChild(QtWidgets.QLabel, 'current_temperature_label')
        temp, bleh = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter a temperature between -25 and 115:')
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")

        try:
            temp = int(temp)
            if (temp <= 115 and temp >= -25):
                tempString = "Current\nTemperature:\n" + str(temp) + " °F"
                TrackModelDef.environmentalTemp = temp
                current_temperature_label.setText(tempString)
                if (temp <= 32):
                    for x in TrackModelDef.trackList:
                        if (x.lineName == "Green" and (not x.trackHeater)):
                            signals.swtrack_set_track_heater.emit(Line.LINE_GREEN, True)
                        elif (x.lineName == "Red" and (not x.trackHeater)):
                            signals.swtrack_set_track_heater.emit(Line.LINE_RED, True)
                        x.setTrackHeater(True)
                    if (not track_heater_button.isChecked()):
                        track_heater_button.toggle()
                        self.update_track_heater()
            else:
                message.setText("Temperature outside of range!\nEnter a value between -25 and 115, inclusive")
                message.exec_()
        except ValueError:
            message.setText("Invalid input: Not an integer")
            message.exec_()

    def set_random_temperature(self):
        randomTemp = random.randrange(-10, 100, 1)
        tempString = "Current\nTemperature:\n" + str(randomTemp) + " °F"
        current_temperature_label = self.findChild(QtWidgets.QLabel, 'current_temperature_label')
        current_temperature_label.setText(tempString)

        TrackModelDef.environmentalTemperature = randomTemp
        track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
        if (randomTemp <= 32):
            for x in TrackModelDef.trackList:
                if (x.lineName == "Green" and (not x.trackHeater)):
                    signals.swtrack_set_track_heater.emit(Line.LINE_GREEN, True)
                elif (x.lineName == "Red" and (not x.trackHeater)):
                    signals.swtrack_set_track_heater.emit(Line.LINE_RED, True)
                x.setTrackHeater(True)
            if (not track_heater_button.isChecked()):
                track_heater_button.toggle()
                self.update_track_heater()
        signals.trackmodel_update_tickets_sold.emit()

    def update_broken_rail_failure(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        theIndex = theTabWidget.currentIndex()
        theLine = theTabWidget.tabText(theIndex)
        theLine = theLine.replace(" Line", "")
        theTrack = TrackModelDef.getTrack(theLine)

        if (theLine == "Green"):
            currentComboBlock = str(combo1.currentText())
            line = Line.LINE_GREEN
        else:
            currentComboBlock = str(combo2.currentText())
            line = Line.LINE_RED

        currentComboBlock = currentComboBlock[6:]

        broken_rail_failure_button = self.findChild(QtWidgets.QPushButton, 'broken_rail_failure_button')
        if (broken_rail_failure_button.isChecked()):
            broken_rail_failure_button.setStyleSheet("background-color: red")
            theTrack.getBlock(int(currentComboBlock)).brokenRailFailure = True
            signals.swtrack_update_broken_rail_failure.emit(line, int(currentComboBlock), True)
        else:
            broken_rail_failure_button.setStyleSheet("background-color: rgb(181, 255, 183)")
            theTrack.getBlock(int(currentComboBlock)).brokenRailFailure = False
            signals.swtrack_update_broken_rail_failure.emit(line, int(currentComboBlock), False)

    def update_power_failure(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        theIndex = theTabWidget.currentIndex()
        theLine = theTabWidget.tabText(theIndex)
        theLine = theLine.replace(" Line", "")
        theTrack = TrackModelDef.getTrack(theLine)

        if (theLine == "Green"):
            currentComboBlock = str(combo1.currentText())
            line = Line.LINE_GREEN
        else:
            currentComboBlock = str(combo2.currentText())
            line = Line.LINE_RED

        currentComboBlock = currentComboBlock[6:]

        power_failure_button = self.findChild(QtWidgets.QPushButton, 'power_failure_button')
        if (power_failure_button.isChecked()):
            power_failure_button.setStyleSheet("background-color: red")
            theTrack.getBlock(int(currentComboBlock)).powerFailure = True
            signals.swtrack_update_power_failure.emit(line, int(currentComboBlock), True)
        else:
            power_failure_button.setStyleSheet("background-color: rgb(181, 255, 183)")
            theTrack.getBlock(int(currentComboBlock)).powerFailure = False
            signals.swtrack_update_power_failure.emit(line, int(currentComboBlock), False)

    def update_track_circuit_failure(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        theIndex = theTabWidget.currentIndex()
        theLine = theTabWidget.tabText(theIndex)
        theLine = theLine.replace(" Line", "")
        theTrack = TrackModelDef.getTrack(theLine)

        if (theLine == "Green"):
            currentComboBlock = str(combo1.currentText())
            line = Line.LINE_GREEN
        else:
            currentComboBlock = str(combo2.currentText())
            line = Line.LINE_RED

        currentComboBlock = currentComboBlock[6:]

        track_circuit_failure_button = self.findChild(QtWidgets.QPushButton, 'track_circuit_failure_button')
        if (track_circuit_failure_button.isChecked()):
            track_circuit_failure_button.setStyleSheet("background-color: red")
            theTrack.getBlock(int(currentComboBlock)).trackCircuitFailure = True
            signals.swtrack_update_track_circuit_failure.emit(line, int(currentComboBlock), True)
        else:
            track_circuit_failure_button.setStyleSheet("background-color: rgb(181, 255, 183)")
            theTrack.getBlock(int(currentComboBlock)).trackCircuitFailure = False
            signals.swtrack_update_track_circuit_failure.emit(line, int(currentComboBlock), False)


    def getFileName(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        
        dialog = QtWidgets.QFileDialog(self)
        fileInfo = dialog.getOpenFileName(self)
        if (".xlsx" in fileInfo[0]):
            records = pyexcel.get_sheet(file_name = fileInfo[0])
            records.name_columns_by_row(0)
            line = records.column['Line'][1]
            totalBlocks = records.number_of_rows()

            TrackModelDef.SignalHandler.readInData(fileInfo)
            self.addTab(line, totalBlocks)
        else:
            message.setText("Incorrect file type! Try again")
            message.exec_()


    def addTab(self, line, totalBlocks):
        global tabsAdded
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        if (line == "Green"):
            theTabWidget.addTab(combo1, line+" Line")
            theCombo = combo1
            combo1.currentIndexChanged.connect(self.switch_block)
            theTabWidget.currentChanged.connect(self.switch_block)
            trackNumber = 0
        else:
            theTabWidget.addTab(combo2, line+" Line")
            theCombo = combo2
            combo2.currentIndexChanged.connect(self.switch_block)
            theTabWidget.currentChanged.connect(self.switch_block)
            trackNumber = 1

        for x in range(totalBlocks):
            theCombo.addItem("Block "+str(x + 1))

        tabsAdded = tabsAdded + 1
        self.show()

    # def check_current_block(self):
    #     theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
    #     if (theTabWidget.tabText(theTabWidget.currentIndex()) == "Green Line"):
    #         combo1.currentIndexChanged.connect(self.switch_block)
    #     elif (theTabWidget.tabText(theTabWidget.currentIndex()) == "Red Line"):
    #         #combo1.currentIndexChanged.connect(self.switch_block)
    #         combo2.currentIndexChanged.connect(self.switch_block)

    def switch_block(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        theIndex = theTabWidget.currentIndex()
        theLine = theTabWidget.tabText(theIndex)
        theLine = theLine.replace(" Line", "")

        if (TrackModelDef.getTrack(theLine) != None):
            theTrack = TrackModelDef.getTrack(theLine)

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
                occupied_label.setText("Occupied by:\n\nTrain "+ str(occupancy))

            switch_list_label = self.findChild(QtWidgets.QLabel, 'switch_list_label')
            switch_list_label.setText("Switches possible:\n\n" + theBlock.getSwitchBlocksString())

            current_switch_label = self.findChild(QtWidgets.QLabel, 'current_switch_label')
            current_switch_label.setText("Switch flipped to:\n\n" + theBlock.getSwitchCurrentString())

            beacon_label = self.findChild(QtWidgets.QLabel, 'beacon_label')
            if (theBlock.blockBeacon == None):
                beacon_label.setText("Beacon:\n\nNone")
            else:
                beacon_label.setText("Beacon:\n"+ theBlock.blockBeacon.station_name+ "/\n" +str(theBlock.blockBeacon.service_brake) +
                 "/\n" + str(theBlock.blockBeacon.DoorSide) + "/\n" + str(theBlock.blockBeacon.lastStation))

            # global trackHeaterButtonSet
            # if (not trackHeaterButtonSet):
            #     track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
            #     track_heater_button.clicked.connect(self.update_track_heater)
            #     trackHeaterButton = True

            track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
            trackHeater = theTrack.trackHeater
            if (trackHeater):
                track_heater_button.setText("On")
                # light green
                track_heater_button.setStyleSheet("background-color: rgb(181, 255, 183)")
                if (not track_heater_button.isChecked()):
                    track_heater_button.toggle()
            else:
                track_heater_button.setText("Off")
                # light red
                track_heater_button.setStyleSheet("background-color: rgb(234, 153, 153)")
                if (track_heater_button.isChecked()):
                    track_heater_button.toggle()

            broken_rail_failure_button = self.findChild(QtWidgets.QPushButton, 'broken_rail_failure_button')
            if (theBlock.brokenRailFailure):
                broken_rail_failure_button.setStyleSheet("background-color: red")
                if (not broken_rail_failure_button.isChecked()):
                    broken_rail_failure_button.toggle()
            else:
                broken_rail_failure_button.setStyleSheet("background-color: rgb(181, 255, 183)")
                if (broken_rail_failure_button.isChecked()):
                    broken_rail_failure_button.toggle()

            power_failure_button = self.findChild(QtWidgets.QPushButton, 'power_failure_button')
            if (theBlock.powerFailure):
                power_failure_button.setStyleSheet("background-color: red")
                if (not power_failure_button.isChecked()):
                    power_failure_button.toggle()
            else:
                power_failure_button.setStyleSheet("background-color: rgb(181, 255, 183)")
                if (power_failure_button.isChecked()):
                    power_failure_button.toggle()

            track_circuit_failure_button = self.findChild(QtWidgets.QPushButton, 'track_circuit_failure_button')
            if (theBlock.trackCircuitFailure):
                track_circuit_failure_button.setStyleSheet("background-color: red")
                if (not track_circuit_failure_button.isChecked()):
                    track_circuit_failure_button.toggle()
            else:
                track_circuit_failure_button.setStyleSheet("background-color: rgb(181, 255, 183)")
                if (track_circuit_failure_button.isChecked()):
                    track_circuit_failure_button.toggle()


            railway_crossing_label = self.findChild(QtWidgets.QLabel, 'railway_crossing_label')
            if (theBlock.blockRailwayCrossing):
                railway_crossing_label.setText("Railway Crossing:\n\nYes")
            else:
                railway_crossing_label.setText("Railway Crossing:\n\nNo")

    def update_track_heater(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        theIndex = theTabWidget.currentIndex()
        theLine = theTabWidget.tabText(theIndex)
        track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')

        if (theLine == "Green Line"):
            theTrack = TrackModelDef.getTrack("Green")
            theLine = Line.LINE_GREEN
        else:
            theTrack = TrackModelDef.getTrack("Red")
            theLine = Line.LINE_RED

        if (not track_heater_button.isChecked()):
            track_heater_button.setText("Off")
            track_heater_button.setStyleSheet("background-color: rgb(234, 153, 153)")
            theTrack.setTrackHeater(False)
            signals.swtrack_set_track_heater.emit(theLine, False)
        else:
            track_heater_button.setText("On")
            track_heater_button.setStyleSheet("background-color: rgb(181, 255, 183)")
            if (not theTrack.trackHeater):
                theTrack.setTrackHeater(True)
                signals.swtrack_set_track_heater.emit(theLine, True)


    def logout(self):
        """Removes this window from the list"""
        window_list.remove(self)

    # def logout(self):
    #     # This is executed when the button is pressed
    #     if(sys.platform == 'darwin'):
    #         os.system('python3 src/UI/login_gui.py &')
    #     else:
    #         os.system('start /B python src/UI/login_gui.py')
    #     app.exit()
