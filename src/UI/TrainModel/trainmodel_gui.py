"""Train Model GUI"""

import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys

sys.path.insert(1, 'src')
from UI.server_functions import *

class Ui(QtWidgets.QMainWindow):
    """UI class for the Train Model"""
    def __init__(self):
        super(Ui, self).__init__()
        self.current_train_id = 1
        self.main_page()

    def main_page(self):
        uic.loadUi('src/UI/TrainModel/main_page.ui', self)

        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_map') 
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'train_button_1')
        self.button.clicked.connect(self.train_menu)
        self.show()

    def train_menu(self):
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Menu.ui', self)
        self.button2 = self.findChild(QtWidgets.QPushButton, 'logout_button_menu') 
        self.button2.clicked.connect(self.logout)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_info_button')
        self.button.clicked.connect(self.train_info_1)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_parameters_button')
        self.button.clicked.connect(self.train_parameters)
        self.button = self.findChild(QtWidgets.QPushButton, 'train_reports_button')
        self.button.clicked.connect(self.train_reports)
        self.button = self.findChild(QtWidgets.QPushButton, 'return_button')
        self.button.clicked.connect(self.main_page)

    def train_info_1(self):

        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page1.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info1') 
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'report_button_info1')
        self.button.clicked.connect(self.train_reports)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page1to2_button') 
        self.logoutbutton.clicked.connect(self.train_info_2)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page1toM_button') 
        self.logoutbutton.clicked.connect(self.train_menu)

        self.disp_command_speed = self.findChild(QtWidgets.QLabel, 'disp_command_speed')

    def train_info_2(self):
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page2.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info2') 
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'report_button_info2')
        self.button.clicked.connect(self.train_reports)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2to1_button') 
        self.logoutbutton.clicked.connect(self.train_info_1)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2to3_button') 
        self.logoutbutton.clicked.connect(self.train_info_3)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2toM_button') 
        self.logoutbutton.clicked.connect(self.train_menu)

    def train_info_3(self):
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page3.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info3') 
        self.logoutbutton.clicked.connect(self.logout)

        self.button = self.findChild(QtWidgets.QPushButton, 'report_button_info3')
        self.button.clicked.connect(self.train_reports)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3to2_button') 
        self.logoutbutton.clicked.connect(self.train_info_2)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3toM_button') 
        self.logoutbutton.clicked.connect(self.train_menu)

    def update_speed(self):
        responsecode, power = send_message(RequestCode.SEND_TRAIN_MODEL_INFO)
        current_speed = power * 2
        responsecode, speed_lim = send_message(RequestCode.GET_SPEED_LIMIT)
        if responsecode == ResponseCode.SUCCESS:
            self.disp_speed_limit.setText(speed_lim + " Km/Hr")
        else:
            self.stopAllTimers()
            print("The server is not running")
        send_message(RequestCode.SET_TRAIN_LENGTH, "1"
                                                      + " " + self.disp_authority_train.text()
                                                      + " " +  self.disp_command_speed.text()
                                                      + " " +  str(current_speed)
                                                      + " " +  self.disp_speed_limit.text())

    def train_parameters(self):
        """Called to used the train parameters page"""
        uic.loadUi('src/UI/TrainModel/train_parameter.ui', self)

        # Find all the elements and connect the methods
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button_parameters')
        logout_button.clicked.connect(self.logout)

        param_to_main_page_button = self.findChild(QtWidgets.QPushButton, 'pagePtoM_button')
        param_to_main_page_button.clicked.connect(self.train_menu)

        save_button = self.findChild(QtWidgets.QPushButton, 'save_button')
        save_button.clicked.connect(self.save_parameters)

    def save_parameters(self):
        """Sends all the entered parameters to the cloud"""
        parameters = { RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_LENGTH : "",
                       RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_MASS : "",
                       RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT : "",
                       RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT : "",
                       RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_WIDTH : "",
                       RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT : ""
        }

        # Get all the text
        parameters[RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_LENGTH] = self.in_length.text()
        parameters[RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_MASS] = self.in_mass.text()
        parameters[RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT] = self.in_height.text()
        parameters[RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT] = self.in_pass.text()
        parameters[RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_WIDTH] = self.in_width.text()
        parameters[RequestCode.TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT] = self.in_crew.text()

        # Verify the user's input
        for value in parameters.values():
            try:
                int(value)
            except ValueError as e:
                self.fail_alert.setStyleSheet("color: red;")
                return

            if value == "":
                self.fail_alert.setStyleSheet("color: red;")
                return

        # Send the data to the cloud
        for request_code, value in parameters.items():
            send_message_async(request_code, str(self.current_train_id) + ' ' + value,
                               lambda *args: None)

        self.save_alert.setStyleSheet("color: green;")
        self.fail_alert.setStyleSheet("color: rgb(133, 158, 166);")

    def train_reports(self):
        """Method called when the train report button is pressed"""
        uic.loadUi('src/UI/TrainModel/Train_Report.ui', self)
        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_report')
        self.logoutbutton.clicked.connect(self.logout)

        self.logoutbutton = self.findChild(QtWidgets.QPushButton, 'pageRtoM_button')
        self.logoutbutton.clicked.connect(self.train_menu)
        self.report_engine_button = self.findChild(QtWidgets.QPushButton, 'report_engine_button')
        self.report_engine_button.clicked.connect(self.report_engine)
        self.report_signal_button = self.findChild(QtWidgets.QPushButton, 'report_signal_button')
        self.report_signal_button.clicked.connect(self.report_signal)
        self.report_brake_button = self.findChild(QtWidgets.QPushButton, 'report_brake_button')
        self.report_brake_button.clicked.connect(self.report_brake)

    def report_engine(self):
        self.alert_sent1.setStyleSheet("color: green;")
        self.alert_sent2.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent3.setStyleSheet("color: rgb(133, 158, 166);")

    def report_signal(self):
        self.alert_sent1.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent2.setStyleSheet("color: green;")
        self.alert_sent3.setStyleSheet("color: rgb(133, 158, 166);")

    def report_brake(self):
        self.alert_sent1.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent2.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent3.setStyleSheet("color: green;")

    @staticmethod
    def logout(self):
        """Method invoked when the logout button is pressed"""
        if(sys.platform == 'darwin'):
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
