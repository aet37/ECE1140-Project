"""Common pages such as a confirmation and alert"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal

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

class DownloadInProgress(QtWidgets.QDialog):
    """Window shown to user while a program is downloading"""

    download_complete = pyqtSignal()
    progress_updated = pyqtSignal(int)
    abort_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/Common/downloading.ui', self)

        self.progress_bar = self.findChild(QtWidgets.QProgressBar, 'progress_bar')

        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'button_box')
        self.abort_button = self.button_box.button(QtWidgets.QDialogButtonBox.Abort)
        self.abort_button.clicked.connect(lambda: self.abort_clicked.emit())

        self.download_complete.connect(self.close)
        self.progress_updated.connect(lambda value: self.progress_bar.setValue(value))

        # Hide help button
        self.setWindowFlags(Qt.WindowTitleHint)
