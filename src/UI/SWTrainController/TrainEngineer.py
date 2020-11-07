import os
from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('src/UI/SWTrainController/TrainEngineer.ui', self)

        #self.submit_in = self.findChild(QtWidgets.QPushButton, 'submit_in') # Find the button
        
        self.button = self.findChild(QtWidgets.QPushButton, 'Logout') # Find the button
        self.button.clicked.connect(self.logout)
        self.button = self.findChild(QtWidgets.QPushButton, 'SaveInputs') # Find the button
        self.button.clicked.connect(self.saveInputs)
        # Create a toggle button
        #self.button = QtWidgets.QPushButton("Toggle", self)

        self.show()

    # Function to return to Controller page
    def logout(self):
        # This is executed when the button is pressed
        if(sys.platform == 'darwin'):
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

    def saveInputs(self):
        # This is executed when the button is pressed
        app.exit()

app = QtWidgets.QApplication(sys.argv)
windows = Ui()
app.exec_()