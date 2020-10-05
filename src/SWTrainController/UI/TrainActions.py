import os
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('/Users/collinhough/Desktop/Classes/JuniorYear/Fall_2020_Classes/ECE1140/Code/UI/TrainActions.ui', self)

        #self.submit_in = self.findChild(QtWidgets.QPushButton, 'submit_in') # Find the button

        # Return to main window button
        self.button = self.findChild(QtWidgets.QPushButton, 'ReturnToMain') # Find the button
        self.button.clicked.connect(self.returnToMain)

        # Vital Function Buttons
        self.button = self.findChild(QtWidgets.QPushButton, 'EmergencyBrake') # Find the button
        self.button.clicked.connect(self.emergencyBrake)
        self.button2 = self.findChild(QtWidgets.QPushButton, 'SetSpeed') # Find the button
        self.button2.clicked.connect(self.setSpeed)
        self.button = self.findChild(QtWidgets.QPushButton, 'ServiceBrake') # Find the button
        self.button.clicked.connect(self.serviceBrake)
        self.button = self.findChild(QtWidgets.QPushButton, 'SetMode') # Find the button
        self.button.clicked.connect(self.setMode)

        # NonVital Function Buttons
        self.button = self.findChild(QtWidgets.QPushButton, 'Doors') # Find the button
        self.button.clicked.connect(self.toggleDoors)
        self.button = self.findChild(QtWidgets.QPushButton, 'Lights') # Find the button
        self.button.clicked.connect(self.toggleLights)
        self.button = self.findChild(QtWidgets.QPushButton, 'SeanPaul') # Find the button
        self.button.clicked.connect(self.changeTemp)
        self.button = self.findChild(QtWidgets.QPushButton, 'Announcements') # Find the button
        self.button.clicked.connect(self.announceStations)
        self.button = self.findChild(QtWidgets.QPushButton, 'Advertisements') # Find the button
        self.button.clicked.connect(self.toggleAds)

        self.show()

    # Function to return to Controller page
    def returnToMain(self):
        # This is executed when the button is pressed
        uic.loadUi('/Users/collinhough/Desktop/Classes/JuniorYear/Fall_2020_Classes/ECE1140/Code/UI/TrainController.ui', self)

    # Vital Function Definitions
    def emergencyBrake(self):
        # This is executed when the button is pressed
        app.exit()
    def setSpeed(self):
        # This is executed when the button is pressed
        app.exit()
    def serviceBrake(self):
        # This is executed when the button is pressed
        app.exit()
    def setMode(self):
        # This is executed when the button is pressed
        app.exit()

    # NonVital Function Definitions
    def toggleDoors(self):
        # This is executed when the button is pressed
        #app.exit()
        print("Hi")
    def toggleLights(self):
        # This is executed when the button is pressed
        app.exit()
    def changeTemp(self):
        # This is executed when the button is pressed
        app.exit()
    def announceStations(self):
        # This is executed when the button is pressed
        app.exit()
    def toggleAds(self):
        # This is executed when the button is pressed
        app.exit()
    

app = QtWidgets.QApplication(sys.argv)
windows = Ui()
app.exec_()