
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
        #self.button.clicked.connect(self.LCDTemp)

        self.button = self.findChild(QtWidgets.QPushButton, 'AdsButton') # Find the button
        self.button.clicked.connect(self.Ads)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'ModeButton') # Find the button
        self.button.clicked.connect(self.Mode)

        self.button = self.findChild(QtWidgets.QPushButton, 'BrakeButton') # Find the button
        #self.button.clicked.connect(self.Progress)

        self.button = self.findChild(QtWidgets.QPushButton, 'FailureButton') # Find the button
        self.button.clicked.connect(self.Failure)

        self.button = self.findChild(QtWidgets.QPushButton, 'SpeedButton')# Find the button
        #self.button.clicked.connect(self.LCDSpeed)

        self.button = self.findChild(QtWidgets.QPushButton, 'PowerButton') # Find the button
        #self.button.clicked.connect(self.LCDPower)

        self.button = self.findChild(QtWidgets.QPushButton, 'KpKiButton') # Find the button
        #self.button.clicked.connect(self.LCDKpKi)

        self.button = self.findChild(QtWidgets.QPushButton, 'PEBrakebutton') # Find the button
        self.button.clicked.connect(self.PEBrake)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'EBrakeButton') # Find the button
        self.button.clicked.connect(self.EBrake)

        
        self.show()

    def Announce(self):
        self.label1 = self.findChild(QtWidgets.QLabel, 'AnnounceLabel')
        if(self.label1.styleSheet()=="color: green;"):
            self.label1.setStyleSheet("color: red;")
        else: 
            self.label1.setStyleSheet("color: green;")

    def Door(self):
        self.label2 = self.findChild(QtWidgets.QLabel, 'DoorLabel')
        if(self.label2.styleSheet()=="color: green;"):
            self.label2.setStyleSheet("color: red;")
        else: 
            self.label2.setStyleSheet("color: green;")

    def Ads(self):
        self.label3 = self.findChild(QtWidgets.QLabel, 'AdsLabel')
        if(self.label3.styleSheet()=="color: green;"):
            self.label3.setStyleSheet("color: red;")
        else: 
            self.label3.setStyleSheet("color: green;")

    def Mode(self):
        self.label4 = self.findChild(QtWidgets.QLabel, 'ModeLabel')
        if(self.label4.styleSheet()=="color: green;"):
            self.label4.setStyleSheet("color: red;")
        else: 
            self.label4.setStyleSheet("color: green;")

    def Failure(self):
        self.label5 = self.findChild(QtWidgets.QLabel, 'BrakeFailure')
        if(self.label5.styleSheet()=="color: green;"):
            self.label5.setStyleSheet("color: red;")
        else: 
            self.label5.setStyleSheet("color: green;")
        self.label6 = self.findChild(QtWidgets.QLabel, 'EngineFailure')
        if(self.label6.styleSheet()=="color: green;"):
            self.label6.setStyleSheet("color: red;")
        else: 
            self.label6.setStyleSheet("color: green;")
        self.label7 = self.findChild(QtWidgets.QLabel, 'SignalFailure')
        if(self.label7.styleSheet()=="color: green;"):
            self.label7.setStyleSheet("color: red;")
        else: 
            self.label7.setStyleSheet("color: green;")
    
    def PEBrake(self):
        self.label8 = self.findChild(QtWidgets.QLabel, 'PEBrakeLabel')
        if(self.label8.styleSheet()=="color: green;"):
            self.label8.setStyleSheet("color: red;")
        else: 
            self.label8.setStyleSheet("color: green;")
    
    def EBrake(self):
        self.label9 = self.findChild(QtWidgets.QLabel, 'EBrakeLabel')
        if(self.label9.styleSheet()=="color: green;"):
            self.label9.setStyleSheet("color: red;")
        else: 
            self.label9.setStyleSheet("color: green;")

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
