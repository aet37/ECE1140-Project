
from PyQt5 import QtWidgets, uic
import sys


class SWTrackControllerUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SWTrackControllerUi, self).__init__()
        uic.loadUi('src/UI/SWTrackController/track_controller.ui', self)

        self.show()
  
app = QtWidgets.QApplication(sys.argv)
window = SWTrackControllerUi()
app.exec_()