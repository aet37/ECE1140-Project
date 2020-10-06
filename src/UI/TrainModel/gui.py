
import os
from PyQt5 import QtWidgets, uic
import sys

# GLOBALS
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.mapPage()
        # uic.loadUi('C:/Users/kenne/Documents/16th Grade/1140 Jerry Seinfeld/Lab 6/Login_Page.ui', self)
        # self.button = self.findChild(QtWidgets.QPushButton, 'login_button')# Find the button
        # self.button.clicked.connect(self.mapPage)
        # self.button2 = self.findChild(QtWidgets.QPushButton, 'logout_button_log') # Find the button
        # self.button2.clicked.connect(self.logout)

        # self.show()
    def mapPage(self):
        uic.loadUi('C:/Users/kenne/Documents/16th Grade/1140 Jerry Seinfeld/Lab 6/Map_Page.ui', self)

        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_map') # Find the button
        self.logoutbutton.clicked.connect(self.logout)
        
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_1')# Find the button
        self.button.clicked.connect(self.train1)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_2') # Find the button
        self.button.clicked.connect(self.train2)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_3') # Find the button
        self.button.clicked.connect(self.train3)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_4') # Find the button
        self.button.clicked.connect(self.train4)
        self.show()
    
    def train1(self):
        # This is executed when the button is pressed
        uic.loadUi('C:/Users/kenne/Documents/16th Grade/1140 Jerry Seinfeld/Lab 6/Train_Menu.ui', self)
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

    def train2(self):
        # This is executed when the button is pressed
        app.exit()
    def train3(self):
        # This is executed when the button is pressed
        app.exit()
    def train4(self):
        # This is executed when the button is pressed
        app.exit()

    def trainInfo1(self):
        # This is executed when the button is pressed
        uic.loadUi('C:/Users/kenne/Documents/16th Grade/1140 Jerry Seinfeld/Lab 6/Train_Info_Page1.ui', self)

    def trainParameters(self):
        # This is executed when the button is pressed
        uic.loadUi('C:/Users/kenne/Documents/16th Grade/1140 Jerry Seinfeld/Lab 6/Train_Parameter.ui', self)

    def trainReports(self):
        # This is executed when the button is pressed
        uic.loadUi('C:/Users/kenne/Documents/16th Grade/1140 Jerry Seinfeld/Lab 6/Train_Report.ui', self)

    def logout(self):
        # This is executed when the button is pressed
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()