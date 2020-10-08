import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
sys.path.insert(1, 'src/UI')
from server_functions import *

class SWTrainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SWTrainUi, self).__init__()
        uic.loadUi('src/UI/SWTrainController/TrainController.ui', self)

        # Create timer to update pages
        self.train_actions_timer = QTimer()
        self.train_actions_timer.timeout.connect(self.update_data)

        # Initialize all buttons and the page of the UI
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.stacked_widget.setCurrentIndex(0)

        # Define which pages buttons will take you to
        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        # Start timer to update train actions page
        self.stopAllTimers()
        self.train_actions_timer.start(250)

        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.return_button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.return_button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Define logout button
        self.logout_button = self.findChild(QtWidgets.QPushButton, 'Logout') # Find the button
        self.logout_button.clicked.connect(self.logout)
        self.logout_button2 = self.findChild(QtWidgets.QPushButton, 'Logout2') # Find the button
        self.logout_button2.clicked.connect(self.logout)
        self.logout_button3 = self.findChild(QtWidgets.QPushButton, 'Logout3') # Find the button
        self.logout_button3.clicked.connect(self.logout)

        self.show()
    
    # Initialize buttons in UI
    def initUI(self):
        # Define buttons on main page
        self.button1 = self.findChild(QtWidgets.QPushButton, 'TrainActions') # Find the button
        self.button2 = self.findChild(QtWidgets.QPushButton, 'Information') # Find the button
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget') # Find stacked widget

        # Define buttons on Train Actions Page
        self.return_button1 = self.findChild(QtWidgets.QPushButton, 'MainMenu2')
        self.doors_button = self.findChild(QtWidgets.QPushButton, 'Doors')
        self.lights_button = self.findChild(QtWidgets.QPushButton, 'Lights')
        self.announceStations_button = self.findChild(QtWidgets.QPushButton, 'Announcements')
        self.ads_button = self.findChild(QtWidgets.QPushButton, 'Advertisements')
        self.automaticMode_button = self.findChild(QtWidgets.QPushButton, 'AutomaticMode')
        self.manualMode_button = self.findChild(QtWidgets.QPushButton, 'ManualMode')
        self.defineToggles()

        #Define buttons on Information Page
        self.return_button2 = self.findChild(QtWidgets.QPushButton, 'MainMenu3')

    def defineToggles(self):
        # Give buttons capability to toggle in appearance
        self.doors_button.setCheckable(True)
        self.doors_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.lights_button.setCheckable(True)
        self.lights_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.announceStations_button.setCheckable(True)
        self.announceStations_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.ads_button.setCheckable(True)
        self.ads_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.automaticMode_button.setCheckable(True)
        self.automaticMode_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.manualMode_button.setCheckable(True)
        self.manualMode_button.setStyleSheet("QPushButton{background-color:rgb(255, 51, 16);}QPushButton:checked{background-color:green;}")

    def set_button_state(self, index):
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.return_button1.setEnabled(True)
        self.return_button2.setEnabled(True)

    def logout(self):
        # This is executed when the button is pressed
        app.exit()

    # Define function to update displayed data
    def update_data(self):
        responseCode, speed = send_message(RequestCode.GET_COMMAND_SPEED)
        if responseCode == ResponseCode.SUCCESS:
            self.CommandSpeedLabel.setText(speed + " MPH")


    def stopAllTimers(self):
        self.train_actions_timer.stop()

app = QtWidgets.QApplication(sys.argv)
windows = SWTrainUi()
app.exec_()