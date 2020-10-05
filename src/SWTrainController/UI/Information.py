import os
from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('/Users/collinhough/Desktop/Classes/JuniorYear/Fall_2020_Classes/ECE1140/Code/UI/Information.ui', self)

        #self.submit_in = self.findChild(QtWidgets.QPushButton, 'submit_in') # Find the button
        
        self.button = self.findChild(QtWidgets.QPushButton, 'ReturnToMain') # Find the button
        self.button.clicked.connect(self.returnToMain)
        self.button = self.findChild(QtWidgets.QPushButton, 'Failures') # Find the button
        self.button.clicked.connect(self.viewFailures)
        self.button = self.findChild(QtWidgets.QPushButton, 'DisplaySchedule') # Find the button
        self.button.clicked.connect(self.displaySchedule)
        
        # Create a toggle button
        #self.button = QtWidgets.QPushButton("Toggle", self)

        self.show()

    # Function to return to Controller page
    def returnToMain(self):
        # This is executed when the button is pressed
        uic.loadUi('/Users/collinhough/Desktop/Classes/JuniorYear/Fall_2020_Classes/ECE1140/Code/UI/TrainController.ui', self)

    def viewFailures(self):
        # This is executed when the button is pressed
        app.exit()
    def displaySchedule(self):
        # This is executed when the button is pressed
        app.exit()

app = QtWidgets.QApplication(sys.argv)
windows = Ui()
app.exec_()