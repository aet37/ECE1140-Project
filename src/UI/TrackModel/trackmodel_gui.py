import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget
import sys
from PyQt5.QtCore import QTimer
sys.path.insert(1, 'src/UI')
from server_functions import *
import pyexcel
import pyexcel_io
import json


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        distance = 0
        # self.track1_info_timer = QTimer()
        # self.track1_info_timer.timeout.connect(self.update_times)
        uic.loadUi('src/UI/TrackModel/Map_Page.ui', self)
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.stacked_widget.setCurrentIndex(0)
        self.block1.clicked.connect(self.page1)
        self.block2.clicked.connect(self.page2)
        self.block3.clicked.connect(self.page3)
        self.block4.clicked.connect(self.page4)
        self.block5.clicked.connect(self.page5)
        self.block6.clicked.connect(self.page6)
        self.block7.clicked.connect(self.page7)
        self.block8.clicked.connect(self.page8)
        self.block9.clicked.connect(self.page9)
        self.block10.clicked.connect(self.page10)
        self.block11.clicked.connect(self.page11)
        self.block12.clicked.connect(self.page12)
        self.block13.clicked.connect(self.page13)
        self.block14.clicked.connect(self.page14)
        self.block15.clicked.connect(self.page15)

        self.signal_1 = self.findChild(QtWidgets.QLabel, 'signal_1')
        self.signal_2 = self.findChild(QtWidgets.QLabel, 'signal_2')
        self.signal_3 = self.findChild(QtWidgets.QLabel, 'signal_3')
        self.signal_4 = self.findChild(QtWidgets.QLabel, 'signal_400')
        self.signal_5 = self.findChild(QtWidgets.QLabel, 'signal_500')
        self.signal_6 = self.findChild(QtWidgets.QLabel, 'signal_600')
        self.signal_7 = self.findChild(QtWidgets.QLabel, 'signal_7')
        self.signal_8 = self.findChild(QtWidgets.QLabel, 'signal_8')
        self.signal_9 = self.findChild(QtWidgets.QLabel, 'signal_9')
        self.signal_10 = self.findChild(QtWidgets.QLabel, 'signal_10')
        self.signal_11 = self.findChild(QtWidgets.QLabel, 'signal_11')
        self.signal_12 = self.findChild(QtWidgets.QLabel, 'signal_12')
        self.signal_13 = self.findChild(QtWidgets.QLabel, 'signal_13')
        self.signal_14 = self.findChild(QtWidgets.QLabel, 'signal_14')
        self.signal_15 = self.findChild(QtWidgets.QLabel, 'signal_15')

        self.speed_limit_1 = self.findChild(QtWidgets.QLabel, 'speed_limit_1')

        self.logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button') # Find the button
        self.logout_button.clicked.connect(self.readInData)

        self.logout_button1 = self.findChild(QtWidgets.QPushButton, 'logout_button1') # Find the button
        self.logout_button1.clicked.connect(self.logout)

        self.logout_button2 = self.findChild(QtWidgets.QPushButton, 'logout_button2') # Find the button
        self.logout_button2.clicked.connect(self.logout)

        self.logout_button3 = self.findChild(QtWidgets.QPushButton, 'logout_button3') # Find the button
        self.logout_button3.clicked.connect(self.logout)

        self.logout_button4 = self.findChild(QtWidgets.QPushButton, 'logout_button4') # Find the button
        self.logout_button4.clicked.connect(self.logout)

        self.logout_button5 = self.findChild(QtWidgets.QPushButton, 'logout_button5') # Find the button
        self.logout_button5.clicked.connect(self.logout)

        self.logout_button6 = self.findChild(QtWidgets.QPushButton, 'logout_button6') # Find the button
        self.logout_button6.clicked.connect(self.logout)

        self.logout_button7 = self.findChild(QtWidgets.QPushButton, 'logout_button7') # Find the button
        self.logout_button7.clicked.connect(self.logout)

        self.logout_button8 = self.findChild(QtWidgets.QPushButton, 'logout_button8') # Find the button
        self.logout_button8.clicked.connect(self.logout)

        self.logout_button9 = self.findChild(QtWidgets.QPushButton, 'logout_button9') # Find the button
        self.logout_button9.clicked.connect(self.logout)

        self.logout_button10 = self.findChild(QtWidgets.QPushButton, 'logout_button10') # Find the button
        self.logout_button10.clicked.connect(self.logout)

        self.logout_button11 = self.findChild(QtWidgets.QPushButton, 'logout_button11') # Find the button
        self.logout_button11.clicked.connect(self.logout)

        self.logout_button12 = self.findChild(QtWidgets.QPushButton, 'logout_button12') # Find the button
        self.logout_button12.clicked.connect(self.logout)

        self.logout_button13 = self.findChild(QtWidgets.QPushButton, 'logout_button13') # Find the button
        self.logout_button13.clicked.connect(self.logout)

        self.logout_button14 = self.findChild(QtWidgets.QPushButton, 'logout_button14') # Find the button
        self.logout_button14.clicked.connect(self.logout)

        self.logout_button15 = self.findChild(QtWidgets.QPushButton, 'logout_button15') # Find the button
        self.logout_button15.clicked.connect(self.logout)



        self.heater_button_1 = self.findChild(QtWidgets.QPushButton, 'heater_button_1')
        self.heater_button_2 = self.findChild(QtWidgets.QPushButton, 'heater_button_2')
        self.heater_button_3 = self.findChild(QtWidgets.QPushButton, 'heater_button_3')
        self.heater_button_4 = self.findChild(QtWidgets.QPushButton, 'heater_button_4')
        self.heater_button_5 = self.findChild(QtWidgets.QPushButton, 'heater_button_5')
        self.heater_button_6 = self.findChild(QtWidgets.QPushButton, 'heater_button_6')
        self.heater_button_7 = self.findChild(QtWidgets.QPushButton, 'heater_button_7')
        self.heater_button_8 = self.findChild(QtWidgets.QPushButton, 'heater_button_8')
        self.heater_button_9 = self.findChild(QtWidgets.QPushButton, 'heater_button_9')
        self.heater_button_10 = self.findChild(QtWidgets.QPushButton, 'heater_button_10')
        self.heater_button_11 = self.findChild(QtWidgets.QPushButton, 'heater_button_11')
        self.heater_button_12 = self.findChild(QtWidgets.QPushButton, 'heater_button_12')
        self.heater_button_13 = self.findChild(QtWidgets.QPushButton, 'heater_button_13')
        self.heater_button_14 = self.findChild(QtWidgets.QPushButton, 'heater_button_14')
        self.heater_button_15 = self.findChild(QtWidgets.QPushButton, 'heater_button_15')

        self.heater_button_1.clicked.connect(self.heater1)
        self.heater_button_2.clicked.connect(self.heater2)
        self.heater_button_3.clicked.connect(self.heater3)
        self.heater_button_4.clicked.connect(self.heater4)
        self.heater_button_5.clicked.connect(self.heater5)
        self.heater_button_6.clicked.connect(self.heater6)
        self.heater_button_7.clicked.connect(self.heater7)
        self.heater_button_8.clicked.connect(self.heater8)
        self.heater_button_9.clicked.connect(self.heater9)
        self.heater_button_10.clicked.connect(self.heater10)
        self.heater_button_11.clicked.connect(self.heater11)
        self.heater_button_12.clicked.connect(self.heater12)
        self.heater_button_13.clicked.connect(self.heater13)
        self.heater_button_14.clicked.connect(self.heater14)
        self.heater_button_15.clicked.connect(self.heater15)
        

        self.back_button_1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_6.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_7.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_8.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_9.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_10.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_11.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_12.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_13.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_14.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.back_button_15.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.show()

    def initUI(self):
        self.block1 = self.findChild(QtWidgets.QPushButton, 'pushButton_1')
        self.block2 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.block3 = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.block4 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.block5 = self.findChild(QtWidgets.QPushButton, 'pushButton_5')
        self.block6 = self.findChild(QtWidgets.QPushButton, 'pushButton_6')
        self.block7 = self.findChild(QtWidgets.QPushButton, 'pushButton_7')
        self.block8 = self.findChild(QtWidgets.QPushButton, 'pushButton_8')
        self.block9 = self.findChild(QtWidgets.QPushButton, 'pushButton_9')
        self.block10 = self.findChild(QtWidgets.QPushButton, 'pushButton_10')
        self.block11 = self.findChild(QtWidgets.QPushButton, 'pushButton_11')
        self.block12 = self.findChild(QtWidgets.QPushButton, 'pushButton_12')
        self.block13 = self.findChild(QtWidgets.QPushButton, 'pushButton_13')
        self.block14 = self.findChild(QtWidgets.QPushButton, 'pushButton_14')
        self.block15 = self.findChild(QtWidgets.QPushButton, 'pushButton_15')
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')

        self.back_button_1 = self.findChild(QtWidgets.QPushButton, 'back_button_1')
        self.back_button_2 = self.findChild(QtWidgets.QPushButton, 'back_button_2')
        self.back_button_3 = self.findChild(QtWidgets.QPushButton, 'back_button_3')
        self.back_button_4 = self.findChild(QtWidgets.QPushButton, 'back_button_4')
        self.back_button_5 = self.findChild(QtWidgets.QPushButton, 'back_button_5')
        self.back_button_6 = self.findChild(QtWidgets.QPushButton, 'back_button_6')
        self.back_button_7 = self.findChild(QtWidgets.QPushButton, 'back_button_7')
        self.back_button_8 = self.findChild(QtWidgets.QPushButton, 'back_button_8')
        self.back_button_9 = self.findChild(QtWidgets.QPushButton, 'back_button_9')
        self.back_button_10 = self.findChild(QtWidgets.QPushButton, 'back_button_10')
        self.back_button_11 = self.findChild(QtWidgets.QPushButton, 'back_button_11')
        self.back_button_12 = self.findChild(QtWidgets.QPushButton, 'back_button_12')
        self.back_button_13 = self.findChild(QtWidgets.QPushButton, 'back_button_13')
        self.back_button_14 = self.findChild(QtWidgets.QPushButton, 'back_button_14')
        self.back_button_15 = self.findChild(QtWidgets.QPushButton, 'back_button_15')

        h_index1 = 0
        h_index2 = 0
        h_index3 = 0
        h_index4 = 0
        h_index5 = 0
        h_index6 = 0
        h_index7 = 0
        h_index8 = 0
        h_index9 = 0
        h_index10 = 0
        h_index11 = 0
        h_index12 = 0
        h_index13 = 0
        h_index14 = 0
        h_index15 = 0
    def page0(self):
        #new_index = self.stacked_widget.currentIndex()-1
        #if new_index >= 0:
        self.stacked_widget.setCurrentIndex(0)

    def page1(self):
        #new_index = self.stacked_widget.currentIndex()+1
        #if new_index < len(self.stacked_widget):
        print('hello')
        self.stacked_widget.setCurrentIndex(1)
        self.trackInfo1()

    def page2(self):
        self.stacked_widget.setCurrentIndex(2)
        self.trackInfo1()

    def page3(self):
        self.stacked_widget.setCurrentIndex(3)
        self.trackInfo1()

    def page4(self):
        self.stacked_widget.setCurrentIndex(4)
        self.trackInfo1()

    def page5(self):
        self.stacked_widget.setCurrentIndex(5)
        self.trackInfo1()

    def page6(self):
        self.stacked_widget.setCurrentIndex(6)
        self.trackInfo1()

    def page7(self):
        self.stacked_widget.setCurrentIndex(7)
        self.trackInfo1()

    def page8(self):
        self.stacked_widget.setCurrentIndex(8)
        self.trackInfo1()

    def page9(self):
        self.stacked_widget.setCurrentIndex(9)
        self.trackInfo1()

    def page10(self):
        self.stacked_widget.setCurrentIndex(10)
        self.trackInfo1()

    def page11(self):
        self.stacked_widget.setCurrentIndex(11)
        self.trackInfo1() 

    def page12(self):
        self.stacked_widget.setCurrentIndex(12)
        self.trackInfo1()

    def page13(self):
        self.stacked_widget.setCurrentIndex(13)
        self.trackInfo1()                                       

    def page14(self):
        self.stacked_widget.setCurrentIndex(14)
        self.trackInfo1()

    def page15(self):
        self.stacked_widget.setCurrentIndex(15)
        self.trackInfo1()

    def set_button_state(self, index):
        i = 0
        #self.block1.setEnabled(True)
        #n_pages = len(self.stacked_widget)
        #self.block2.setEnabled(True)
        #self.block3.setEnabled(True)

    def heater1(self, h_index1):
        h_index1 = h_index1 + 1;
        if (h_index1 % 2 == 0):
            self.heater_button_1.setText('On')
            self.heater_button_1.setStyleSheet("background-color : green")
        else:
            self.heater_button_1.setText('Off')
            self.heater_button_1.setStyleSheet("background-color : rgb(255,0,0)")

    def heater2(self, h_index2):
        h_index2 = h_index2 + 1;
        if (h_index2 % 2 == 0):
            self.heater_button_2.setText('On')
            self.heater_button_2.setStyleSheet("background-color : green")
        else:
            self.heater_button_2.setText('Off')
            self.heater_button_2.setStyleSheet("background-color : rgb(255,0,0)")

    def heater3(self, h_index3):
        h_index3 = h_index3 + 1;
        if (h_index3 % 2 == 0):
            self.heater_button_3.setText('On')
            self.heater_button_3.setStyleSheet("background-color : green")
        else:
            self.heater_button_3.setText('Off')
            self.heater_button_3.setStyleSheet("background-color : rgb(255,0,0)") 

    def heater4(self, h_index4):
        h_index4 = h_index4 + 1;
        if (h_index4 % 2 == 0):
            self.heater_button_4.setText('On')
            self.heater_button_4.setStyleSheet("background-color : green")
        else:
            self.heater_button_4.setText('Off')
            self.heater_button_4.setStyleSheet("background-color : rgb(255,0,0)") 

    def heater5(self, h_index5):
        h_index5 = h_index5 + 1;
        if (h_index5 % 2 == 0):
            self.heater_button_5.setText('On')
            self.heater_button_5.setStyleSheet("background-color : green")
        else:
            self.heater_button_5.setText('Off')
            self.heater_button_5.setStyleSheet("background-color : rgb(255,0,0)")

    def heater6(self, h_index6):
        h_index6 = h_index6 + 1;
        if (h_index6 % 2 == 0):
            self.heater_button_6.setText('On')
            self.heater_button_6.setStyleSheet("background-color : green")
        else:
            self.heater_button_6.setText('Off')
            self.heater_button_6.setStyleSheet("background-color : rgb(255,0,0)")

    def heater7(self, h_index7):
        h_index7 = h_index7 + 1;
        if (h_index7 % 2 == 0):
            self.heater_button_7.setText('On')
            self.heater_button_7.setStyleSheet("background-color : green")
        else:
            self.heater_button_7.setText('Off')
            self.heater_button_7.setStyleSheet("background-color : rgb(255,0,0)")

    def heater8(self, h_index8):
        h_index8 = h_index8 + 1;
        if (h_index8 % 2 == 0):
            self.heater_button_8.setText('On')
            self.heater_button_8.setStyleSheet("background-color : green")
        else:
            self.heater_button_8.setText('Off')
            self.heater_button_8.setStyleSheet("background-color : rgb(255,0,0)")

    def heater9(self, h_index9):
        h_index9 = h_index9 + 1;
        if (h_index9 % 2 == 0):
            self.heater_button_9.setText('On')
            self.heater_button_9.setStyleSheet("background-color : green")
        else:
            self.heater_button_9.setText('Off')
            self.heater_button_9.setStyleSheet("background-color : rgb(255,0,0)")

    def heater10(self, h_index10):
        h_index10 = h_index10 + 1;
        if (h_index10 % 2 == 0):
            self.heater_button_10.setText('On')
            self.heater_button_10.setStyleSheet("background-color : green")
        else:
            self.heater_button_10.setText('Off')
            self.heater_button_10.setStyleSheet("background-color : rgb(255,0,0)")

    def heater11(self, h_index11):
        h_index11 = h_index11 + 1;
        if (h_index11 % 2 == 0):
            self.heater_button_11.setText('On')
            self.heater_button_11.setStyleSheet("background-color : green")
        else:
            self.heater_button_11.setText('Off')
            self.heater_button_11.setStyleSheet("background-color : rgb(255,0,0)")

    def heater12(self, h_index12):
        h_index12 = h_index12 + 1;
        if (h_index12 % 2 == 0):
            self.heater_button_12.setText('On')
            self.heater_button_12.setStyleSheet("background-color : green")
        else:
            self.heater_button_12.setText('Off')
            self.heater_button_12.setStyleSheet("background-color : rgb(255,0,0)")

    def heater13(self, h_index13):
        h_index13 = h_index13 + 1;
        if (h_index13 % 2 == 0):
            self.heater_button_13.setText('On')
            self.heater_button_13.setStyleSheet("background-color : green")
        else:
            self.heater_button_13.setText('Off')
            self.heater_button_13.setStyleSheet("background-color : rgb(255,0,0)")

    def heater14(self, h_index14):
        h_index14 = h_index14 + 1;
        if (h_index14 % 2 == 0):
            self.heater_button_14.setText('On')
            self.heater_button_14.setStyleSheet("background-color : green")
        else:
            self.heater_button_14.setText('Off')
            self.heater_button_14.setStyleSheet("background-color : rgb(255,0,0)")

    def heater15(self, h_index15):
        h_index15 = h_index15 + 1;
        if (h_index15 % 2 == 0):
            self.heater_button_15.setText('On')
            self.heater_button_15.setStyleSheet("background-color : green")
        else:
            self.heater_button_15.setText('Off')
            self.heater_button_15.setStyleSheet("background-color : rgb(255,0,0)")
    
    def update_times(self):
        # TODO get position string from Train Model in ??? UNITS
        # position_string = send_message(RequestCode.GET_POSITION_FROM_TRAINM)

        # convert position string to an int
        # int position = std::stoi(position_string)


        send_message(RequestCode.GET_POSITION_FROM_TRAINM)


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
            stationList = []
            switchList = []
            trackInfo['Track'] = ''
            trackInfo['Total Blocks'] = records.number_of_rows()
            trackInfo['Stations'] = stationList
            trackInfo['Switches'] = switchList
            trackInfo['Block List'] = ''
            blockList = []
            # stations = 0;
            for x in range(records.number_of_rows()):
                destinationSwitchList = ''
                blockStation = ''
                # print('%s Line | Section %c | Block Number %d | Block Length (m) %d | Block Grade (%%) %d | Speed Limit (Km/Hr) %d | Stations %s | Switches %s | Elevation (m) %d | Cumulative Elevation (m) %d' % (records.column['Line'][x], records.column['Section'][x], records.column['Block Number'][x], records.column['Block Length (m)'][x], records.column['Block Grade (%)'][x], records.column['Speed Limit (Km/Hr)'][x], records.column['Stations'][x], records.column['Switches'][x], records.column['Elevation (m)'][x], records.column['Cumulative Elevation (m)'][x]))
                # line = records.column['Line'][x]
                blockNumber = records.column['Block Number'][x]
                
                # Set line name
                line = records.column['Line'][x]
                trackInfo['Track'] = line


                # Get station lists
                if (records.column['Stations'][x] != ""):
                    #stations = stations + 1
                    stationSplit = records.column['Stations'][x].split(' ', 1) # now have station name
                    stationList.append({'blockNumber':blockNumber, 'station':stationSplit[1]})
                    blockStation = stationSplit[1]
                    trackInfo['Stations'] = stationList
                    
                    # Get switch lists
                if (records.column['Switches'][x] != ""):
                    cutString = records.column['Switches'][x].replace('SWITCH (', '').replace(' ', '').replace(')', '')
                    testList = cutString.split('-')
                    if (int(testList[0]) == blockNumber | int(testList[0:1] == blockNumber) | int(testList[0:2] == blockNumber)):
                        splitString = cutString.split(';')
                        destinationSwitchList = []
                        for y in range(len(splitString)):
                            destinationSwitchList.append(int(splitString[y].replace(str(blockNumber)+'-', '')))
                        switchList.append({'switchBase':blockNumber, 'switchDestinations':destinationSwitchList})
                        trackInfo['Switches'] = switchList


                # set block info
                blockLength = records.column['Block Length (m)'][x]
                blockGrade = records.column['Block Grade (%)'][x]
                blockSpeedLimit = records.column['Speed Limit (Km/Hr)'][x]
                blockStation = blockStation
                blockSwitch = destinationSwitchList
                blockElevation = records.column['Elevation (m)'][x]
                blockCumulativeElevation = records.column['Cumulative Elevation (m)'][x]

                blockList.append({'blockNumber':blockNumber, 'blockLength':blockLength, 'blockGrade':blockGrade, 'blockSpeedLimit':blockSpeedLimit, 'blockStation':blockStation, 'blockSwitch':blockSwitch, 'blockElevation':blockElevation, 'blockCumulativeElevation':blockCumulativeElevation})
            trackInfo['Block List'] = blockList
            #print(trackInfo)
            jsonString = json.dumps(trackInfo)
            stringLength = len(jsonString)
            i = 0
            stringToPrint = ''
            print('stringLength = '+str(stringLength))
            send_message(RequestCode.SEND_TRACK_OCCUPANCY_TO_SW_TRACK_C, str(jsonString[0:1000]))
            # while (stringLength > 0):
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
