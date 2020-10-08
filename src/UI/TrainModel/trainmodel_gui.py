
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
sys.path.insert(1, 'src/UI')
from server_functions import *

#import CTC

username = "trainmodel"
password = "jerry"

# GLOBALS
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.train1_info_timer = QTimer()
        self.train1_info_timer.timeout.connect(self.update_speed)
        self.mapPage()

    def mapPage(self):
        self.stopAllTimers()
        uic.loadUi('src/UI/TrainModel/Map_Page.ui', self)

        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_map') # Find the button
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_1')# Find the button
        self.button.clicked.connect(self.trainMenu1)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_2') # Find the button
        self.button.clicked.connect(self.trainMenu2)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_3') # Find the button
        self.button.clicked.connect(self.trainMenu3)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_4') # Find the button
        self.button.clicked.connect(self.trainMenu4)
        self.show()

    def trainMenu1(self):
        self.stopAllTimers()
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Menu.ui', self)
        self.button2 = self.findChild(QtWidgets.QPushButton, 'logout_button_menu') # Find the button
        self.button2.clicked.connect(self.logout)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_info_button')# Find the button
        self.button.clicked.connect(self.trainInfo1)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_parameters_button')# Find the button
        self.button.clicked.connect(self.trainParameters)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_reports_button')# Find the button
        self.button.clicked.connect(self.trainReports)
        self.button = self.findChild(QtWidgets.QPushButton, 'return_button')# Find the button
        self.button.clicked.connect(self.mapPage)

    def trainMenu2(self):
        # This is executed when the button is pressed
        app.exit()
    def trainMenu3(self):
        # This is executed when the button is pressed
        app.exit()
    def trainMenu4(self):
        # This is executed when the button is pressed
        app.exit()

    def trainInfo1(self):
        self.stopAllTimers()
        
        self.train1_info_timer.start(250)

        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page1.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info1') # Find the button
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'report_button_info1')# Find the button
        self.button.clicked.connect(self.trainReports)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page1to2_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainInfo2)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page1toM_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainMenu1)

        self.disp_command_speed = self.findChild(QtWidgets.QLabel, 'disp_command_speed')# Find the button
    def trainInfo2(self):
        self.stopAllTimers()
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page2.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info2') # Find the button
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'report_button_info2')# Find the button
        self.button.clicked.connect(self.trainReports)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2to1_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainInfo1)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2to3_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainInfo3)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2toM_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainMenu1)

    def trainInfo3(self):
        self.stopAllTimers()
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page3.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info3') # Find the button
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'report_button_info3')# Find the button
        self.button.clicked.connect(self.trainReports)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3to2_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainInfo2)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3toM_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainMenu1)

    def update_speed(self):
        responsecode, speed = send_message(RequestCode.GET_COMMAND_SPEED)
        if responsecode == ResponseCode.SUCCESS:
            self.disp_command_speed.setText(speed + " MPH")
        else:
            self.stopAllTimers()
            print("The server is not running")

    def trainParameters(self):
        self.stopAllTimers()
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Parameter.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_parameters') # Find the button
        self.logoutbutton.clicked.connect(self.logout)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'pagePtoM_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainMenu1)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'save_button') # Find the button
        self.logoutbutton.clicked.connect(self.saveParameters)

    def saveParameters(self):
        #save parameters
        self.save_alert.setStyleSheet("color: green;")
        send_message(RequestCode.SET_TRAIN_LENGTH, self.in_length.text())

    def trainReports(self):
        self.stopAllTimers()
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Report.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_report') # Find the button
        self.logoutbutton.clicked.connect(self.logout)

        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'pageRtoM_button') # Find the button
        self.logoutbutton.clicked.connect(self.trainMenu1)
        self.report_engine_button = self.findChild(QtWidgets.QPushButton, 'report_engine_button')# Find the button
        self.report_engine_button.clicked.connect(self.reportEngine)
        self.report_signal_button = self.findChild(QtWidgets.QPushButton, 'report_signal_button')# Find the button
        self.report_signal_button.clicked.connect(self.reportSignal)
        self.report_brake_button = self.findChild(QtWidgets.QPushButton, 'report_brake_button')# Find the button
        self.report_brake_button.clicked.connect(self.reportBrake)

    def reportEngine(self):
        self.alert_sent1.setStyleSheet("color: green;")
        self.alert_sent2.setStyleSheet("color: rgb(221, 221, 221);")
        self.alert_sent3.setStyleSheet("color: rgb(221, 221, 221);")

    def reportSignal(self):
        self.alert_sent1.setStyleSheet("color: rgb(221, 221, 221);")
        self.alert_sent2.setStyleSheet("color: green;")
        self.alert_sent3.setStyleSheet("color: rgb(221, 221, 221);")

    def reportBrake(self):
        self.alert_sent1.setStyleSheet("color: rgb(221, 221, 221);")
        self.alert_sent2.setStyleSheet("color: rgb(221, 221, 221);")
        self.alert_sent3.setStyleSheet("color: green;")

    def logout(self):
        # This is executed when the button is pressed
        if(sys.platform == 'darwin'):
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

    def stopAllTimers(self):
        self.train1_info_timer.stop()

# Main Login Screen
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()         # Exit from login screen
