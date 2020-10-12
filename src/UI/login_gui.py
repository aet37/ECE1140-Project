
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
        uic.loadUi('src/UI/Login_Page.ui', self)
        self.alert_login = self.findChild(QtWidgets.QLabel, 'alert_login')
        self.username_in = self.findChild(QtWidgets.QLineEdit, 'username_in')
        self.password_in = self.findChild(QtWidgets.QLineEdit, 'password_in')

        self.button = self.findChild(QtWidgets.QPushButton, 'login_button')# Find the button
        self.button.clicked.connect(self.loginParse)
        self.button = self.findChild(QtWidgets.QPushButton, 'TurnOff') # Find the button
        self.button.clicked.connect(self.Leave)
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
            if(sys.platform == 'darwin'):
                os.system('python3 src/UI/TrackModel/trackmodel_gui.py &')
            else:
                os.system('start /B python src/UI/TrackModel/trackmodel_gui.py')
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
            if(sys.platform == 'darwin'):
                os.system('python3 src/UI/SWTrainController/TrainController.py &')
            else:
                os.system('start /B python src/UI/TrainController/TrainController.py')
            app.exit()
        elif username == "engineer" and password == "jerry":
            if(sys.platform == 'darwin'):
                os.system('python3 src/UI/SWTrainController/TrainEngineer.py &')
            else:
                os.system('start /B python src/UI/TrainController/TrainEngineer.py')
            app.exit()
        else:
            self.alert_login.setStyleSheet("color: red;")

    def Leave(self):
    	# Exit application
    	app.exit()

# Main Login Screen
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()         # Exit from login screen
