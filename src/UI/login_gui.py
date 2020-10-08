
import os
from PyQt5 import QtWidgets, uic
import sys

#import CTC

username = "trainmodel"
password = "jerry"

# GLOBALS
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.login()


    def login(self):
        uic.loadUi('src/UI/TrainModel/Login_Page.ui', self)
        self.alert_login = self.findChild(QtWidgets.QLabel, 'alert_login')
        self.username_in = self.findChild(QtWidgets.QLineEdit, 'username_in')
        self.password_in = self.findChild(QtWidgets.QLineEdit, 'password_in')

        self.button = self.findChild(QtWidgets.QPushButton, 'login_button')# Find the button
        self.button.clicked.connect(self.loginParse)
        self.show()

    def loginParse(self):
        username = self.username_in.text()
        password = self.password_in.text()
        if username == "trainmodel" and password == "jerry":
            if(sys.platform == 'darwin'):
                os.system('python3 src/UI/TrainModel/trainmodel_gui.py &')
            else:
                os.system('start /B python src/UI/TrainModel/trainmodel_gui.py')
            app.exit()
        elif username == "trackmodel" and password == "jerry":
<<<<<<< HEAD
            if(sys.platform == 'darwin'):
                os.system('python3 src/UI/TrackModel/gui.py &')
            else:
                os.system('start /B python src/UI/TrackModel/gui.py')
=======
            os.system('start /B python src/UI/TrackModel/trackmodel_gui.py')
>>>>>>> master
            app.exit()
        elif username == "hwtrack" and password == "jerry":
            print("hwtrack")
        elif username == "swtrack" and password == "jerry":
            print("swtrack")
        elif username == "ctc" and password == "jerry":
            if(sys.platform == 'darwin'):
                os.system('python3 src/UI/CTC/ctc_gui.py &')
            else:
                os.system('start /B python src/UI/CTC/ctc_gui.py')
            app.exit()
        elif username == "hwtrain" and password == "jerry":
            print("hwtrain")
        elif username == "swtrain" and password == "jerry":
            print("swtrain")
        else:
            self.alert_login.setStyleSheet("color: red;")

# Main Login Screen
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()         # Exit from login screen
