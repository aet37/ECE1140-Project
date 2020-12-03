"""Extra page for debug operations"""

from PyQt5 import QtWidgets, uic

class DebugUi(QtWidgets.QMainWindow):
    """Page shown to user upon application startup"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/debug.ui', self)

        self.upload_tracks_button = self.findChild(QtWidgets.QPushButton, 'upload_tracks_button')
        self.download_plc_programs_button = self.findChild(QtWidgets.QPushButton, 'download_plc_programs_button')

        self.upload_tracks_button.clicked.connect(self.upload_tracks)
        self.download_plc_programs_button.clicked.connect(self.download_plc_programs)

        self.show()

    def upload_tracks(self):
        """Auto uploads the red and green lines"""
        self.upload_tracks_button.setEnabled(False)

        from main import auto_upload_tracks
        auto_upload_tracks()

    def download_plc_programs(self):
        """Downloads all the plc programs to the track controllers"""
        self.download_plc_programs_button.setEnabled(False)

        from main import auto_download_plc_programs
        auto_download_plc_programs()
