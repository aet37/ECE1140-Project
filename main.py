
import sys
from PyQt5 import QtWidgets

from src.UI.login_gui import LoginUi
from src.UI.window_manager import window_list

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window_list.append(LoginUi())

    app.exec_()