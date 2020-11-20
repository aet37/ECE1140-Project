"""GUI class for the timekeeper"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QButtonGroup

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

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton, 'one_times_button'))
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton, 'two_times_button'))
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton, 'five_times_button'))
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton, 'ten_times_button'))
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton, 'fifty_times_button'))
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton, 'one_hundred_times_button'))

        self.button_group.buttonClicked.connect(self.update_speed)

        self.show()

    def update_time(self, day, hours, mins, secs):
        """Updates the time label

        :param int day: Current day
        :param int hours: Current hours
        :param int mins: Current minutes
        :param int secs: Current seconds

        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time_text = "{} {:02}:{:02}:{:02}".format(days[day], hours, mins, secs)

        time_label = self.findChild(QtWidgets.QLabel, 'time_label')
        time_label.setText(time_text)

    def update_speed(self):
        """Method called when a new speed factor is selected

        Note: Button ids start at -2 and go down for some god awful reason
        """
        periods = [1, 0.5, 0.2, 0.1, 0.05, 0.01]

        with timekeeper.run_lock:
            timekeeper.timer_period_in_sec = periods[abs(self.button_group.checkedId()) - 2]
