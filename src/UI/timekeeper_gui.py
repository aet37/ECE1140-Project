"""Main page displayed to the user when they start the application"""

from PyQt5 import QtWidgets, uic

class TimekeeperUi(QtWidgets.QMainWindow):
    """Page shown to user upon application startup"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/timekeeper.ui', self)

        self.show()
