"""Module defining signals for communications"""

from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    lights_toggled = pyqtSignal(bool)

# Single instance to be used by other modules
signals = SignalsClass()
