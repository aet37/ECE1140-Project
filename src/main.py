
import sys
from PyQt5 import QtWidgets

from UI.login_gui import LoginUi
from UI.window_manager import window_list

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window_list.append(LoginUi())

    app.exec_()