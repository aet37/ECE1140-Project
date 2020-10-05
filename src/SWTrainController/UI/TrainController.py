import os
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('/Users/collinhough/Desktop/Classes/JuniorYear/Fall_2020_Classes/ECE1140/Code/UI/TrainController.ui', self)

        #self.submit_in = self.findChild(QtWidgets.QPushButton, 'submit_in') # Find the button
        self.button = self.findChild(QtWidgets.QPushButton, 'TrainActions') # Find the button
        self.button.clicked.connect(self.trainActions)
        self.button = self.findChild(QtWidgets.QPushButton, 'Information') # Find the button
        self.button.clicked.connect(self.information)
        
        # Create a toggle button
        #self.button = QtWidgets.QPushButton("Toggle", self)


        self.button2 = self.findChild(QtWidgets.QPushButton, 'Logout') # Find the button
        self.button2.clicked.connect(self.logout)

        self.show()

    def trainActions(self):
        # This is executed when the button is pressed
        app.exit()
    def information(self):
        # This is executed when the button is pressed
        app.exit()
    def logout(self):
        # This is executed when the button is pressed
        app.exit()

app = QtWidgets.QApplication(sys.argv)
windows = Ui()
app.exec_()