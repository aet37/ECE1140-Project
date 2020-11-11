import os
import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QLabel, QComboBox
import sys
from PyQt5.QtCore import QTimer
sys.path.insert(1, 'src')
from UI.server_functions import *
import pyexcel
import pyexcel_io
import json
tracks = 0



class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        # self.track1_info_timer = QTimer()
        # self.track1_info_timer.timeout.connect(self.update_times)

        uic.loadUi('src/UI/TrackModel/Map_Page.ui', self)

        self.show()
        global combo1
        combo1 = QComboBox()
        global combo2 
        combo2 = QComboBox()
        global combo3 
        combo3 = QComboBox()

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

        track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
        track_heater_button.clicked.connect(self.trackHeaterGUI)

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
        global tracks
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
                
                tracks = tracks + 1
                # set track nmumber inside of trackInfo dictionary
                trackInfo['tNumber'] = tracks - 1

                # set totalBlocks inside trackInfo
                trackInfo['Total Blocks'] = records.number_of_rows()

                jsonString = json.dumps(trackInfo)
                send_message(RequestCode.TRACK_MODEL_GUI_TRACK_LAYOUT, str(jsonString))
                #print(str(jsonString))


                theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
                line = records.column['Line'][1]
                #combo1.addItem("Select "+line+" Line block")
                if (tracks == 1):
                    theTabWidget.addTab(combo1, line+" Line")
                    theCombo = combo1
                elif (tracks == 2):
                    theTabWidget.addTab(combo2, line+" Line")
                    theCombo = combo2
                else:
                    theTabWidget.addTab(combo3, line+" Line")
                    theCombo = combo3


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

                    blockInfo['Track'] = tracks - 1
                    blockInfo['Number'] = blockNumber
                    blockInfo['Length'] = blockLength
                    blockInfo['Grade'] = blockGrade
                    blockInfo['Speed Limit'] = blockSpeedLimit
                    blockInfo['Elevation'] = blockElevation
                    blockInfo['Cumulative Elevation'] = blockCumulativeElevation
                    blockInfo['Direction'] = blockDirection


                    if (records.column['Underground'][x] != ""):
                        blockInfo['Underground'] = "true"
                    else:
                        blockInfo['Underground']= "false"

                    blockInfo['Section'] = blockSection

                    if (records.column['Stations'][x] != ""):
                        blockInfo['Station'] = records.column['Stations'][x]
                        blockInfo['Exit Side'] = records.column['Exit Side'][x]

                    if (records.column['Switches'][x] != ""):
                        blockInfo['Switches'] = records.column['Switches'][x]

                    if (records.column['Railway Crossing'][x] != ""):
                        blockInfo['Railway Crossing'] = "true"
                    else:
                        blockInfo['RailwayCrossing'] = "false"

                    jsonString = json.dumps(blockInfo)
                    #print(jsonString)
                    send_message(RequestCode.TRACK_MODEL_GUI_BLOCK, str(jsonString))

                self.send_gather_data_message()

            else:
                print('error')
    def check_current_block(self):
        if (tracks == 1):
            combo1.currentIndexChanged.connect(self.send_gather_data_message)
        elif(tracks == 2):
            combo1.currentIndexChanged.connect(self.send_gather_data_message)
            combo2.currentIndexChanged.connect(self.send_gather_data_message)

    def send_gather_data_message(self):
        """Method called periodically to send the gather data message to the server"""
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        if (theTabWidget.currentIndex() == 0):
            currentComboBlock = str(combo1.currentText())
        elif(theTabWidget.currentIndex() == 1):
            currentComboBlock = str(combo2.currentText())
        else:
            currentComboBlock = str(combo3.currentText())

        lineNumber = (theTabWidget.currentIndex())
        currentComboBlock = currentComboBlock[6:]

        data = str(lineNumber) + " " + str(currentComboBlock)
        send_message_async(RequestCode.TRACK_MODEL_GUI_GATHER_DATA, data=data, callback=self.update_gui)

    def update_gui(self, response_code, response_data):
        if response_code == ResponseCode.ERROR:
            print("There was a problem communicating with the server")
            return

        # line name, block number, section, elevation, cumulative elevation
        # length, grade, speed limit, underground, stationName
        # ticketsSold, passengersBoarded, passengersExited, exit side, occupied by
        # switchList, currentSwitch, trackHeater, failure mode
        
        split_data = response_data.split(' ')

        lineName = split_data[0]
        blockNumber = int(split_data[1])
        section = split_data[2]
        elevation = float(split_data[3])
        cumulativeElevation = float(split_data[4])
        length = float(split_data[5])
        grade = float(split_data[6])
        speedLimit = int(split_data[7])
        underground = split_data[8]
        stationName = split_data[9]

        stationName = stationName.replace('_', ' ')

        ticketsSold = int(split_data[10])
        passengersBoarded = int(split_data[11])
        passengersExited = int(split_data[12])
        exitSide = split_data[13]
        occupied = int(split_data[14])
        switchList1 = int(split_data[15])
        switchList2 = int(split_data[16])
        currentSwitch = int(split_data[17])
        trackHeater = split_data[18]
        failureMode = split_data[19]



        line_name_label = self.findChild(QtWidgets.QLabel, 'line_name_label')
        line_name_label.setText(lineName + " Line")

        block_number_label = self.findChild(QtWidgets.QLabel, 'block_number_label')
        block_number_label.setText("Block " + str(blockNumber))

        section_label = self.findChild(QtWidgets.QLabel, 'section_label')
        section_label.setText("Section: " + section)

        elevation_label = self.findChild(QtWidgets.QLabel, 'elevation_label')
        elevation_label.setText("Elevation\n\n"+ str(elevation)+ " m")

        cumulative_elevation_label = self.findChild(QtWidgets.QLabel, 'cumulative_elevation_label')
        cumulative_elevation_label.setText("Cumulative Elevation\n\n"+ str(cumulativeElevation)+ " m")

        length_label = self.findChild(QtWidgets.QLabel, 'length_label')
        length_label.setText("Block Length:\n\n"+ str(length)+ " m")

        grade_label = self.findChild(QtWidgets.QLabel, 'grade_label')
        grade_label.setText("Block Grade:\n\n"+ str(grade)+'%')

        speed_limit_label = self.findChild(QtWidgets.QLabel, 'speed_limit_label')
        speed_limit_label.setText("Speed Limit:\n\n"+ str(speedLimit)+" Km/Hr")

        underground_label = self.findChild(QtWidgets.QLabel, 'underground_label')
        underground_label.setText("Underground:\n\n"+ str(underground))

        station_name_label = self.findChild(QtWidgets.QLabel, 'station_name_label')
        station_name_label.setText("Station Name:\n\n"+ stationName)

        tickets_sold_label = self.findChild(QtWidgets.QLabel, 'tickets_sold_label')
        tickets_sold_label.setText("Tickets Sold:\n\n"+ str(ticketsSold))

        passengers_boarded_label = self.findChild(QtWidgets.QLabel, 'passengers_boarded_label')
        passengers_boarded_label.setText("Passengers Boarded:\n\n"+ str(passengersBoarded))

        passengers_exited_label = self.findChild(QtWidgets.QLabel, 'passengers_exited_label')
        passengers_exited_label.setText("Passengers Exited:\n\n"+ str(passengersExited))

        exit_side_label = self.findChild(QtWidgets.QLabel, 'exit_side_label')
        exit_side_label.setText("Exit Side:\n\n"+ exitSide)

        occupied_label = self.findChild(QtWidgets.QLabel, 'occupied_label')
        if (occupied == -1):
            occupied_label.setText("Occupied by:\n\nNone")
        else:
            occupied_label.setText("Occupied by:\n\n"+ str(occupied))

        switch_list_label = self.findChild(QtWidgets.QLabel, 'switch_list_label')
        if (switchList1 == -1):
            switch_list_label.setText("Switches possible:\n\nNA")
        else:
            switch_list_label.setText("Switches possible:\n\n"+ str(switchList1) +' '+ str(switchList2))

        current_switch_label = self.findChild(QtWidgets.QLabel, 'current_switch_label')

        if (currentSwitch == -1):
            current_switch_label.setText("Switch flipped to:\n\nNA")
        else:
            current_switch_label.setText("Switch flipped to: \n\n"+str(currentSwitch))


        track_heater_button = self.findChild(QtWidgets.QPushButton, 'track_heater_button')
        if (trackHeater == "true"):
            track_heater_button.setText("On")
            track_heater_button.setStyleSheet("background-color : green")
        else:
            track_heater_button.setText("Off")
            track_heater_button.setStyleSheet("background-color : red")

        failure_mode_label = self.findChild(QtWidgets.QLabel, 'failure_mode_label')
        failure_mode_label.setText("Failure Mode:\n\n"+ failureMode)

    def trackHeaterGUI(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        lineIndex = theTabWidget.currentIndex()

        track_heater_button = self.findChild(QWidget.QPushButton, 'track_heater_button')
        
        if (track_heater_button.isChecked()):
            heaterInput = True
        else:
            heaterInput = False

        if (trackHeater == "true"):
            track_heater_button.setText("On")
            track_heater_button.setStyleSheet("background-color : green")
        else:
            track_heater_button.setText("Off")
            track_heater_button.setStyleSheet("background-color : red")

        send_message(RequestCode.TRACK_MODEL_GUI_SET_HEATER, lineIndex, heaterInput)


    def trackInfo1(self):
        self.stopAllTimers()
        self.track1_info_timer.start(1000)

    def stopAllTimers(self):
        self.track1_info_timer.stop()

    def logout(self):
        # This is executed when the button is pressed
        if(sys.platform == 'darwin'):
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
