"""Common pages such as a confirmation and alert"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

class Alert(QtWidgets.QDialog):
    """Page shown to user to alert them to something"""
    def __init__(self, message):
        super().__init__()
        uic.loadUi('src/UI/Common/alert.ui', self)

        # Find label and set its text
        message_label = self.findChild(QtWidgets.QLabel, 'message_label')
        message_label.setText(message)

        # Hide help button
        self.setWindowFlags(Qt.WindowCloseButtonHint)

class Confirmation(QtWidgets.QDialog):
    """Page shown to user to get their confirmation"""
    def __init__(self, message):
        super().__init__()
        uic.loadUi('src/UI/Common/confirmation.ui', self)

        # Find label and set its text
        message_label = self.findChild(QtWidgets.QLabel, 'message_label')
        message_label.setText(message)

        # Hide help button
        self.setWindowFlags(Qt.WindowCloseButtonHint)
