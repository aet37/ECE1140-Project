import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget
import sys
from PyQt5.QtCore import QTimer
sys.path.insert(1, 'src/UI')
from server_functions import *


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.track1_info_timer = QTimer()
        self.track1_info_timer.timeout.connect(self.update_times)
        uic.loadUi('src/TrackModel/Map_Page.ui', self)
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
        self.logout_button.clicked.connect(self.logout)

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
        responsecode, times = send_message(RequestCode.GET_SIGNAL_TIMES)
        if responsecode == ResponseCode.SUCCESS:
            times = times.split(" ")
            self.signal_1.setText('Signal Last\nTripped:\n'+times[0])
            self.signal_2.setText('Signal Last\nTripped:\n'+times[1])
            self.signal_3.setText('Signal Last\nTripped:\n'+times[2])
            self.signal_4.setText('Signal Last\nTripped:\n'+times[3])
            self.signal_5.setText('Signal Last\nTripped:\n'+times[4])
            self.signal_6.setText('Signal Last\nTripped:\n'+times[5])
            self.signal_7.setText('Signal Last\nTripped:\n'+times[6])
            self.signal_8.setText('Signal Last\nTripped:\n'+times[7])
            self.signal_9.setText('Signal Last\nTripped:\n'+times[8])
            self.signal_10.setText('Signal Last\nTripped:\n'+times[9])
            self.signal_11.setText('Signal Last\nTripped:\n'+times[10])
            self.signal_12.setText('Signal Last\nTripped:\n'+times[11])
            self.signal_13.setText('Signal Last\nTripped:\n'+times[12])
            self.signal_14.setText('Signal Last\nTripped:\n'+times[13])
            self.signal_15.setText('Signal Last\nTripped:\n'+times[14])
        else:
            print(responsecode)
        responsecode, switch = send_message(RequestCode.GET_SWITCH_POSITION)
        if responsecode == ResponseCode.SUCCESS:
            switch = switch.split(" ")
            self.switch_5.setText('Switch flipped to:\n\n'+switch[0])
        else:
            self.stopAllTimers()
            print('The server is not running')

        send_message(RequestCode.SET_SPEED_LIMIT, self.speed_limit_1.text()[46:48])

        responsecode, speed = send_message(RequestCode.GET_SPEED_LIMIT)
        if responsecode == ResponseCode.SUCCESS:
            print(speed)
        else:
            print('fail')

    def trackInfo1(self):
        self.stopAllTimers()
        self.track1_info_timer.start(5000)

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
