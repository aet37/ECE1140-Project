"""GUI class for the timekeeper"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QButtonGroup

from src.signals import signals
from src.timekeeper import timekeeper

PERIODS = [1, 0.5, 0.2, 0.1, 0.05, 0.01]

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
        self.button_group.addButton(self.findChild(QtWidgets.QPushButton,
                                                   'one_hundred_times_button'))

        # Set the correct button according to the time factor
        self.button_group.button(PERIODS.index(timekeeper.time_factor)*-1 - 2) \
                                 .setChecked(True)

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

        period = 'am'
        if hours in range(12, 24):
            period = 'pm'

        if hours > 12:
            hours -= 12

        time_text = "{} {:02}:{:02}:{:02} {}".format(days[day], hours, mins, secs, period)

        time_label = self.findChild(QtWidgets.QLabel, 'time_label')
        time_label.setText(time_text)

    def update_speed(self):
        """Method called when a new speed factor is selected

        Note: Button ids start at -2 and go down for some god awful reason
        """
        # We don't need the lock here because this variable is only being used for the sleep time
        timekeeper.time_factor = PERIODS[abs(self.button_group.checkedId()) - 2]
