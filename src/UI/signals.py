from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

class SignalsObject(QObject):
    lights_toggled = pyqtSignal(bool)


Signals = SignalsObject()