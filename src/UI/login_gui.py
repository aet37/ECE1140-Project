"""Main page displayed to the user when they start the application"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

from src.UI.window_manager import window_list
from src.timekeeper import timekeeper
from src.UI.timekeeper_gui import TimekeeperUi
from src.UI.CTC.ctc_gui import CTCUi
from src.UI.SWTrackController.swtrack_gui import SWTrackControllerUi
from src.UI.TrackModel.trackmodel_gui import TrackModelUi
from src.UI.TrainModel.trainmodel_gui import TrainModelUi
from src.UI.SWTrainController.TrainController import SWTrainUi

class LoginUi(QtWidgets.QMainWindow):
    """Page shown to user upon application startup"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/login_page.ui', self)

        self.alert_login = self.findChild(QtWidgets.QLabel, 'alert_login')
        self.username_in = self.findChild(QtWidgets.QLineEdit, 'username_in')
        self.password_in = self.findChild(QtWidgets.QLineEdit, 'password_in')

        self.login_button = self.findChild(QtWidgets.QPushButton, 'login_button')
        self.login_button.clicked.connect(self.login_parse)

        self.show()

    def login_parse(self):
        """Checks the user's credentials and starts the specific module's ui if correct"""
        username = self.username_in.text()
        password = self.password_in.text()

        if username == "trainmodel" and password == "jerry":
            window_list.append(TrainModelUi())
        elif username == "trackmodel" and password == "jerry":
            window_list.append(TrackModelUi())
        elif username == "swtrack" and password == "jerry":
            window_list.append(SWTrackControllerUi())
        elif username == "ctc" and password == "jerry":
            window_list.append(CTCUi())
        elif username == "swtrain" and password == "jerry":
            window_list.append(SWTrainUi())
        elif username == "timekeeper" and password == "jerry":
            window_list.append(TimekeeperUi())
        else:
            self.alert_login.setStyleSheet("color: red;")
            return

    # pylint: disable=invalid-name
    def keyPressEvent(self, event):
        """Handles a keypress event"""
        if event.key() not in (Qt.Key_Enter, Qt.Key_Return):
            super().keyPressEvent(event)
        else:
            self.login_parse()

    def closeEvent(self, event):
        """Method to run when the login page is closed"""
        # Close all the windows
        window_list.clear()
