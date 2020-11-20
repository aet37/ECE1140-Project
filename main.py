"""Main file to run"""

import sys
from PyQt5 import QtWidgets

from src.UI.login_gui import LoginUi
from src.UI.window_manager import window_list
from src.timekeeper import timekeeper

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window_list.append(LoginUi())

    # Start the timekeeper
    timekeeper.start_time()

    app.exec_()
