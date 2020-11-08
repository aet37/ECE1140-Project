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

        self.initUI()
        #self.stacked_widget.currentChanged.connect(self.set_button_state)
        #self.stacked_widget.setCurrentIndex(0)



        self.show()
    def initUI(self):
        theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
        #self.button.clicked.connect(self.trainMenu1)
        addTrackButton = self.findChild(QtWidgets.QPushButton, 'add_track_button')
        addTrackButton.clicked.connect(self.readInData)
    # def addTab(self):
    #     tab = QtWidgets.QMainWindow()
    #     self.tabWidget.addTab(tab, "Red Line")
    #     w = Ui()
    #     w.show()
    #     sys.exit(app.exec_())

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
                print(str(jsonString))


                theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
                combo1 = QComboBox()
                line = records.column['Line'][1]
                combo1.addItem("Select "+line+" Line block")
                theTabWidget.addTab(combo1, line+" Line")

                for x in range(records.number_of_rows()):
                    blockInfo = {}
                    blockNumber = records.column['Block Number'][x]
                    combo1.addItem("Block "+str(blockNumber)) 

                    blockLength = records.column['Block Length (m)'][x]
                    blockGrade = records.column['Block Grade (%)'][x]
                    blockSpeedLimit = records.column['Speed Limit (Km/Hr)'][x]
                    #blockStation = blockStation
                    #blockSwitch = destinationSwitchList
                    blockElevation = records.column['Elevation (m)'][x]
                    blockCumulativeElevation = round(records.column['Cumulative Elevation (m)'][x], 2)


                    blockInfo['Number'] = blockNumber
                    blockInfo['Length'] = blockLength
                    blockInfo['Grade'] = blockGrade
                    blockInfo['Speed Limit'] = blockSpeedLimit
                    blockInfo['Elevation'] = blockElevation
                    blockInfo['Cumulative Elevation'] = blockCumulativeElevation

                    if (records.column['Stations'][x] != ""):
                        blockInfo['Station'] = records.column['Stations'][x]
                        blockInfo['Exit Side'] = records.column['Exit Side'][x]
                    if (records.column['Switches'][x] != ""):
                        switchString = records.column['Switches'][x]
                        #switchString = switchString.split(',')
                        blockInfo['Switches'] = switchString
                    if (records.column['Underground'][x] != ""):
                        blockInfo['Underground'] = "true"
                    if (records.column['Railway Crossing'][x] != ""):
                        blockInfo['Railway Crossing'] = "true"

                    print(blockInfo)
                    jsonString = json.dumps(blockInfo)
                    send_message(RequestCode.TRACK_MODEL_GUI_BLOCK, str(jsonString))

            else:
                print('error')

            # for x in range(records.number_of_rows() + 1):

            #     destinationSwitchList = ''
            #     blockStation = ''
            #     # print('%s Line | Section %c | Block Number %d | Block Length (m) %d | Block Grade (%%) %d | Speed Limit (Km/Hr) %d | Stations %s | Switches %s | Elevation (m) %d | Cumulative Elevation (m) %d' % (records.column['Line'][x], records.column['Section'][x], records.column['Block Number'][x], records.column['Block Length (m)'][x], records.column['Block Grade (%)'][x], records.column['Speed Limit (Km/Hr)'][x], records.column['Stations'][x], records.column['Switches'][x], records.column['Elevation (m)'][x], records.column['Cumulative Elevation (m)'][x]))
            #     # line = records.column['Line'][x]
            #     blockNumber = records.column['Block Number'][x]
                
            #     # Set line name
            #     line = records.column['Line'][x]
            #     trackInfo['Track'] = line

            #     # Get station lists
            #     if (records.column['Stations'][x] != ""):
            #         #stations = stations + 1
            #         stationSplit = records.column['Stations'][x].split(' ', 1) # now have station name
            #         stationList.append({'blockNumber':blockNumber, 'station':stationSplit[1]})
            #         blockStation = stationSplit[1]
            #         trackInfo['Stations'] = stationList
                    
            #         # Get switch lists
            #     if (records.column['Switches'][x] != ""):
            #         cutString = records.column['Switches'][x].replace('SWITCH (', '').replace(' ', '').replace(')', '')
            #         testList = cutString.split('-')
            #         if (int(testList[0]) == blockNumber | int(testList[0:1] == blockNumber) | int(testList[0:2] == blockNumber)):
            #             splitString = cutString.split(';')
            #             destinationSwitchList = []
            #             for y in range(len(splitString)):
            #                 destinationSwitchList.append(int(splitString[y].replace(str(blockNumber)+'-', '')))
            #             switchList.append({'switchBase':blockNumber, 'switchDestinations':destinationSwitchList})
            #             trackInfo['Switches'] = switchList

            #     if (x == 1):
            #         theTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget_hello')
            #         combo1 = QComboBox()
            #         combo1.addItem("Select "+line+" Line block")
            #         theTabWidget.addTab(combo1, line+" Line")            

            #     combo1.addItem("Block "+str(blockNumber))
            # trackInfo['Block List'] = blockList


            #print(trackInfo)
            # jsonString = json.dumps(trackInfo)
            # stringLength = len(jsonString)
            # i = 0
            # stringToPrint = ''
            # print('stringLength = '+str(stringLength))
            # send_message(RequestCode.TRACK_MODEL_GUI_TRACK_LAYOUT_START, str(jsonString[0:1000]))
            # # while (stringLength > 0):
            #     if (i == 0 & (stringLength > 1000)):
            #         print('1')
            #         i = 1
            #         stringToPrint = '----'+jsonString[0:1000]
            #         stringLength = stringLength - 1000
            #         jsonString = jsonString[1000:]
            #         send_message(RequestCode.SET_SPEED_LIMIT, stringToPrint)
            #         print(stringToPrint)
            #     elif (i == 0):
            #         print('2')
            #         i = 1
            #         stringToPrint = '----'+jsonString+'----'
            #         send_message(RequestCode.SET_SPEED_LIMIT, stringToPrint)
            #         print(stringToPrint)
            #     elif (stringLength < 1000):
            #         print('3')
            #         stringToPrint = jsonString+'----'
            #         stringLength = 0
            #         send_message(RequestCode.SET_SPEED_LIMIT, stringToPrint)
            #         print(stringToPrint)
            #     else:
            #         print('4')
            #         stringToPrint = jsonString[0:1000]
            #         stringLength = stringLength - 1000
            #         jsonString = jsonString[1000:]
            #         send_message(RequestCode.SET_SPEED_LIMIT, stringToPrint)
            #         print(stringToPrint)
                    



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
