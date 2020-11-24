import os
import sys
import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QLabel, QComboBox
from PyQt5.QtCore import QTimer
#from src.UI.server_functions import *
#from src.UI.window_manager import window_list
import json
import pyexcel
import pyexcel_io
sys.path.append(".")
from src.TrackModel import TrackModelDef
from src.signals import *
from src.UI.window_manager import window_list


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

        self.initUI()
        #self.stacked_widget.currentChanged.connect(self.set_button_state)
        #self.stacked_widget.setCurrentIndex(0)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.switch_block)
        self.update_timer.start(3000)

        self.show()

        # signals.trackmodel_update_occupancy.connect(self.updateOccupancy)

    def initUI(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        #self.button.clicked.connect(self.trainMenu1)
        addTrackButton = self.findChild(QtWidgets.QPushButton, 'add_track_button')
        addTrackButton.clicked.connect(self.getFileName)

        logoutButton = self.findChild(QtWidgets.QPushButton, 'logout_button')
        logoutButton.clicked.connect(self.logout)

    def getFileName(self):
        dialog = QtWidgets.QFileDialog(self)
        fileInfo = dialog.getOpenFileName(self)
        records = pyexcel.get_sheet(file_name = fileInfo[0])
        records.name_columns_by_row(0)
        line = records.column['Line'][1]
        totalBlocks = records.number_of_rows()
        
        TrackModelDef.SignalHandler.readInData(fileInfo)
        self.addTab(line, totalBlocks)
    
    def addTab(self, line, totalBlocks):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        if (line == "Green"):
            theTabWidget.addTab(combo1, line+" Line")
            theCombo = combo1
            trackNumber = 0
        elif (line == "Red"):
            theTabWidget.addTab(combo2, line+" Line")
            theCombo = combo2
            trackNumber = 1

        for x in range(totalBlocks):
            theCombo.addItem("Block "+str(x + 1))
    
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

