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
                trackInfo['tNumber'] = tracks

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

                    blockInfo['Track'] = tracks
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

    def send_gather_data_message(self):
        """Method called periodically to send the gather data message to the server"""
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        if (theTabWidget.currentIndex() == 0):
            currentComboBlock = str(combo1.currentText())
        elif(theTabWidget.currentIndex() == 1):
            currentComboBlock = str(combo2.currentText())
        else:
            currentComboBlock = str(combo3.currentText())

        lineNumber = (theTabWidget.currentIndex() + 1)
        currentComboBlock = currentComboBlock[6:]

        data = str(lineNumber) + " " + str(currentComboBlock)
        send_message_async(RequestCode.TRACK_MODEL_GUI_GATHER_DATA, data=data, callback=self.update_gui)

    def update_gui(self, response_code, response_data):
        print("test123")
        if response_code == ResponseCode.ERROR:
            print("There was a problem communicating with the server")
            return
        

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
