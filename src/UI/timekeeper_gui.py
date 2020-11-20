"""GUI class for the timekeeper"""

from time import time
from PyQt5 import QtWidgets, uic

from src.signals import signals
from src.timekeeper import timekeeper

class TimekeeperUi(QtWidgets.QMainWindow):
    """User interface for the timekeeper"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/timekeeper.ui', self)

        self.pause_button = self.findChild(QtWidgets.QPushButton, 'pause_button')
        self.pause_button.clicked.connect(timekeeper.pause_time)

        self.start_button = self.findChild(QtWidgets.QPushButton, 'start_button')
        self.start_button.clicked.connect(timekeeper.resume_time)

        signals.timer_expired.connect(self.update_time)

        self.update_time(timekeeper.current_day,
                         timekeeper.current_time_hour,
                         timekeeper.current_time_min,
                         timekeeper.current_time_sec)

        self.show()

    def update_time(self, day, hours, mins, secs):
        """Updates the time label

        :param int hours: Current hours
        :param int mins: Current minutes
        :param int secs: Current seconds

        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time_text = "{} {:02}:{:02}:{:02}".format(days[day], hours, mins, secs)

        time_label = self.findChild(QtWidgets.QLabel, 'time_label')
        time_label.setText(time_text)
