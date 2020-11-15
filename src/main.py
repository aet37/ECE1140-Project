
import sys
from PyQt5 import QtWidgets

from UI.login_gui import LoginPage
from UI.window_manager import window_list

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window_list.append(LoginPage())

    app.exec_()