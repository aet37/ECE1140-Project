"""Main page displayed to the user when they start the application"""

import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

from UI.window_manager import window_list
from UI.TrainModel.trainmodel_gui import TrainModelUi
from UI.SWTrainController.TrainController import SWTrainUi
class LoginPage(QtWidgets.QMainWindow):
    """Page shown to user upon application startup"""
    def __init__(self):
        super().__init__()
        self.login()

    def login(self):
        """Loads the login page ui and displays it"""
        uic.loadUi('src/UI/Login_Page.ui', self)
        self.alert_login = self.findChild(QtWidgets.QLabel, 'alert_login')
        self.username_in = self.findChild(QtWidgets.QLineEdit, 'username_in')
        self.password_in = self.findChild(QtWidgets.QLineEdit, 'password_in')

        self.button = self.findChild(QtWidgets.QPushButton, 'login_button')# Find the button
        self.button.clicked.connect(self.login_parse)
        self.button = self.findChild(QtWidgets.QPushButton, 'TurnOff') # Find the button
        self.button.clicked.connect(self.stuff)
        self.show()

    def stuff(self):
        print(window_list.remove(self))

    def login_parse(self):
        """Checks the user's credentials and starts the specific module's ui if correct"""
        username = self.username_in.text()
        password = self.password_in.text()
        file_path = ''
        if username == "trainmodel" and password == "jerry":
            window_list.append(TrainModelUi())
        elif username == "trackmodel" and password == "jerry":
            file_path = 'src/UI/TrackModel/trackmodel_gui.py'
        elif username == "swtrack" and password == "jerry":
            file_path = 'src/UI/SWTrackController/sw_track_gui.py'
        elif username == "ctc" and password == "jerry":
            file_path = 'src/UI/CTC/ctc_gui.py'
        elif username == "hwtrain" and password == "jerry":
            print("hwtrain")
        elif username == "swtrain" and password == "jerry":
            window_list.append(SWTrainUi())
        elif username == "engineer" and password == "jerry":
            file_path = 'src/UI/SWTrainController/TrainEngineer.py'
        else:
            self.alert_login.setStyleSheet("color: red;")
            return

        # window_list.remove(self)

    def keyPressEvent(self, event): # pylint: disable=invalid-name
        """Handles a keypress event"""
        if event.key() not in (Qt.Key_Enter, Qt.Key_Return):
            super().keyPressEvent(event)
        else:
            self.login_parse()
