
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
sys.path.insert(1, 'src')
from UI.server_functions import *

#import CTC

username = "hwtrain"
password = "jerry"

# GLOBALS
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.train1_info_timer = QTimer()
        self.HW_Train_Controller() # Change map page to my page name

    def HW_Train_Controller(self): # change map page
        self.stopAllTimers()
        uic.loadUi('src/UI/HWTrainController/HW_Train_Controller.ui', self)

        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'Logout') # Find the button
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'AnnounceButton')# Find the button
        self.button.clicked.connect(self.Announce)

        self.button = self.findChild(QtWidgets.QPushButton, 'DoorButton') # Find the button
        self.button.clicked.connect(self.Door)

        self.button = self.findChild(QtWidgets.QPushButton, 'TempButton') # Find the button
        self.button.clicked.connect(self.Temp)

        self.button = self.findChild(QtWidgets.QPushButton, 'AdsButton') # Find the button
        self.button.clicked.connect(self.Ads)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'ModeButton') # Find the button
        self.button.clicked.connect(self.Mode)

        self.button = self.findChild(QtWidgets.QPushButton, 'BrakeButton') # Find the button
        self.button.clicked.connect(self.Brake)

        self.button = self.findChild(QtWidgets.QPushButton, 'BrakeFailButton') # Find the button
        self.button.clicked.connect(self.BrakeFailure)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'EngineFailButton') # Find the button
        self.button.clicked.connect(self.EngineFailure)

        self.button = self.findChild(QtWidgets.QPushButton, 'SignalFailButton') # Find the button
        self.button.clicked.connect(self.SignalFailure)

        self.button = self.findChild(QtWidgets.QPushButton, 'SpeedButton')# Find the button
        self.button.clicked.connect(self.Speed)

        self.button = self.findChild(QtWidgets.QPushButton, 'PowerButton') # Find the button
        self.button.clicked.connect(self.Power)

        self.button = self.findChild(QtWidgets.QPushButton, 'KpButton') # Find the button
        self.button.clicked.connect(self.Kp)

        self.button = self.findChild(QtWidgets.QPushButton, 'KiButton') # Find the button
        self.button.clicked.connect(self.Ki)

        self.button = self.findChild(QtWidgets.QPushButton, 'PEBrakebutton') # Find the button
        self.button.clicked.connect(self.PEBrake)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'EBrakeButton') # Find the button
        self.button.clicked.connect(self.EBrake)

        self.button = self.findChild(QtWidgets.QPushButton, 'LightsButton') # Find the button
        self.button.clicked.connect(self.Lights)
        
        
        self.show()

    def Announce(self):
        self.label1 = self.findChild(QtWidgets.QLabel, 'AnnounceLabel')
        if(self.label1.styleSheet()=="color: green;"):
            self.label1.setStyleSheet("color: red;")
            self.label1.setText("Off")
            send_message(RequestCode.HWTRAIN_ANNOUNCE_STATIONS, "0")
        else: 
            self.label1.setStyleSheet("color: green;")
            self.label1.setText("On")
            send_message(RequestCode.HWTRAIN_ANNOUNCE_STATIONS, "1")

    def Door(self):
        self.label2 = self.findChild(QtWidgets.QLabel, 'DoorLabel')
        if(self.label2.styleSheet()=="color: green;"):
            self.label2.setStyleSheet("color: red;")
            self.label2.setText("Off")
            send_message(RequestCode.HWTRAIN_TOGGLE_DAMN_DOORS, "0")
        else: 
            self.label2.setStyleSheet("color: green;")
            self.label2.setText("On")
            send_message(RequestCode.HWTRAIN_TOGGLE_DAMN_DOORS, "1")

    def Ads(self):
        self.label3 = self.findChild(QtWidgets.QLabel, 'AdsLabel')
        if(self.label3.styleSheet()=="color: green;"):
            self.label3.setStyleSheet("color: red;")
            self.label3.setText("Off")
            send_message(RequestCode.HWTRAIN_DISPLAY_ADS, "0")
        else: 
            self.label3.setStyleSheet("color: green;")
            self.label3.setText("On")
            send_message(RequestCode.HWTRAIN_DISPLAY_ADS, "1")

    def Mode(self):
        self.label4 = self.findChild(QtWidgets.QLabel, 'ModeLabel')
        if(self.label4.styleSheet()=="color: green;"):
            self.label4.setStyleSheet("color: red;")
            self.label4.setText("Off")
            send_message(RequestCode.HWTRAIN_GUI_GET_MODE, "0")
        else: 
            self.label4.setStyleSheet("color: green;")
            self.label4.setText("On")
            send_message(RequestCode.HWTRAIN_GUI_GET_MODE, "1")

    def BrakeFailure(self):
        self.label5 = self.findChild(QtWidgets.QLabel, 'BrakeFailureLabel')
        if(self.label5.styleSheet()=="color: green;"):
            self.label5.setStyleSheet("color: red;")
            self.label5.setText("Off")
            send_message(RequestCode.HWTRAIN_BRAKE_FAILURE, "0")
        else: 
            self.label5.setStyleSheet("color: green;")
            self.label5.setText("On")
            send_message(RequestCode.HWTRAIN_BRAKE_FAILURE, "1")

    def EngineFailure(self):
        self.label6 = self.findChild(QtWidgets.QLabel, 'EngineFailureLabel')
        if(self.label6.styleSheet()=="color: green;"):
            self.label6.setStyleSheet("color: red;")
            self.label6.setText("Off")
            send_message(RequestCode.HWTRAIN_ENGINE_FAILURE, "0")
        else: 
            self.label6.setStyleSheet("color: green;")
            self.label6.setText("On")
            send_message(RequestCode.HWTRAIN_ENGINE_FAILURE, "1")

    def SignalFailure(self):
        self.label7 = self.findChild(QtWidgets.QLabel, 'SignalFailureLabel')
        if(self.label7.styleSheet()=="color: green;"):
            self.label7.setStyleSheet("color: red;")
            self.label7.setText("Off")
            send_message(RequestCode.HWTRAIN_SIGNAL_FAILURE, "0")
        else: 
            self.label7.setStyleSheet("color: green;")
            self.label7.setText("On")
            send_message(RequestCode.HWTRAIN_SIGNAL_FAILURE, "1")
    
    def PEBrake(self):
        self.label8 = self.findChild(QtWidgets.QLabel, 'PEBrakeLabel')
        if(self.label8.styleSheet()=="color: green;"):
            self.label8.setStyleSheet("color: red;")
            self.label8.setText("Off")
            send_message(RequestCode.HWTRAIN_PULL_PASSENGER_EBRAKE, "0")
        else: 
            self.label8.setStyleSheet("color: green;")
            self.label8.setText("On")
            send_message(RequestCode.HWTRAIN_PULL_PASSENGER_EBRAKE, "1")
    
    def EBrake(self):
        self.label9 = self.findChild(QtWidgets.QLabel, 'EBrakeLabel')
        if(self.label9.styleSheet()=="color: green;"):
            self.label9.setStyleSheet("color: red;")
            self.label9.setText("Off")
            send_message(RequestCode.HWTRAIN_PULL_EBRAKE, "0")
        else: 
            self.label9.setStyleSheet("color: green;")
            self.label9.setText("On")
            send_message(RequestCode.HWTRAIN_PULL_EBRAKE, "1")

    def Brake(self):
        self.label10 = self.findChild(QtWidgets.QLabel, 'BrakeLabel')
        if(self.label10.styleSheet()=="color: green;"):
            self.label10.setStyleSheet("color: red;")
            self.label10.setText("Off")
            send_message(RequestCode.HWTRAIN_PRESS_SERVICE_BRAKE, "0")
        else: 
            self.label10.setStyleSheet("color: green;")
            self.label10.setText("On")
            send_message(RequestCode.HWTRAIN_PRESS_SERVICE_BRAKE, "1")
    
    def Lights(self):
        self.label11 = self.findChild(QtWidgets.QLabel, 'LightsLabel')
        if(self.label11.styleSheet()=="color: green;"):
            self.label11.setStyleSheet("color: red;")
            self.label11.setText("Off")
            send_message(RequestCode.HWTRAIN_TOGGLE_CABIN_LIGHTS, "0")
        else: 
            self.label11.setStyleSheet("color: green;")
            self.label11.setText("On")
            send_message(RequestCode.HWTRAIN_TOGGLE_CABIN_LIGHTS, "1")

    def Temp(self):
        self.LCD1 = self.findChild(QtWidgets.QLCDNumber, 'TempLCD')
        self.LCD1.display(1.22)
        send_message(RequestCode.HWTRAIN_SET_TEMPERATURE, "1")

    def Speed(self):
        self.LCD2 = self.findChild(QtWidgets.QLCDNumber, 'SpeedLCD')
        self.LCD2.display(2.44)
        send_message(RequestCode.HWTRAIN_UPDATE_CURRENT_SPEED, "1")

    def Power(self):
        self.LCD3 = self.findChild(QtWidgets.QLCDNumber, 'PowerLCD')
        self.LCD3.display(3.66)
        send_message(RequestCode.HWTRAIN_GUI_DISPLAY_POWER, "1")
        
    def Kp(self):
        self.LCD4 = self.findChild(QtWidgets.QLCDNumber, 'KpLCD')
        self.LCD4.display(4.88)
        send_message(RequestCode.HWTRAIN_GUI_SET_KP, "1")

    def Ki(self):
        self.LCD5 = self.findChild(QtWidgets.QLCDNumber, 'KiLCD')
        self.LCD5.display(6)
        send_message(RequestCode.HWTRAIN_GUI_SET_KI, "1")

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
