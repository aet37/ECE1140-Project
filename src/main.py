
import sys
from PyQt5 import QtWidgets

from UI.login_gui import LoginPage
from UI.window_manager import window_list

# Import singleton instances of modules
from include.SWTrainController.ControlSystem import control_system

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window_list.append(LoginPage())

    app.exec_()