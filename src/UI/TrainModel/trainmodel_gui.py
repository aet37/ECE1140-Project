"""Train Model GUI"""

import os
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QTimer
import sys

sys.path.insert(1, 'src')
from UI.server_functions import send_message_async, RequestCode

class Ui(QtWidgets.QMainWindow):
    """UI class for the Train Model"""
    def __init__(self):
        super(Ui, self).__init__()
        self.current_train_id = 1
        self.train_menu()

    #######################################################################
    ############################## GUI PAGES ##############################
    #######################################################################
    def train_menu(self):
        """Method called after a train is selected"""
        uic.loadUi('src/UI/TrainModel/Train_Menu.ui', self)

        # TESTING DYNAMIC SCREEN SIZE!!!!!!!!!!!!!
        # screen = app.primaryScreen()
        # print('Screen: %s' % screen.name())
        # size = screen.size()
        # print('Size: %d x %d' % (size.width(), size.height()))
        # rect = screen.availableGeometry()
        # print('Available: %d x %d' % (rect.width(), rect.height()))
        # TESTING DYNAMIC SCREEN SIZE!!!!!!!!!!!!!

        # Find all elements and connect them accordingly
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button_menu')
        logout_button.clicked.connect(self.logout)

        train_info_button = self.findChild(QtWidgets.QPushButton, 'train_info_button')
        train_info_button.clicked.connect(self.train_info_1)

        train_parameters_button = self.findChild(QtWidgets.QPushButton, 'train_parameters_button')
        train_parameters_button.clicked.connect(self.train_parameters)

        train_reports_button = self.findChild(QtWidgets.QPushButton, 'train_reports_button')
        train_reports_button.clicked.connect(self.train_reports)

        # Show the page
        self.show()

    def train_info_1(self):

        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page1.ui', self)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info1')
        logoutbutton.clicked.connect(self.logout)

        button = self.findChild(QtWidgets.QPushButton, 'report_button_info1')
        button.clicked.connect(self.train_reports)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page1to2_button')
        logoutbutton.clicked.connect(self.train_info_2)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page1toM_button')
        logoutbutton.clicked.connect(self.train_menu)

        disp_command_speed = self.findChild(QtWidgets.QLabel, 'disp_command_speed')

    def train_info_2(self):
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page2.ui', self)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info2')
        logoutbutton.clicked.connect(self.logout)

        button = self.findChild(QtWidgets.QPushButton, 'report_button_info2')
        button.clicked.connect(self.train_reports)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2to1_button')
        logoutbutton.clicked.connect(self.train_info_1)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2to3_button')
        logoutbutton.clicked.connect(self.train_info_3)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page2toM_button')
        logoutbutton.clicked.connect(self.train_menu)

    def train_info_3(self):
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page3.ui', self)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info3')
        logoutbutton.clicked.connect(self.logout)

        button = self.findChild(QtWidgets.QPushButton, 'report_button_info3')
        button.clicked.connect(self.train_reports)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3to2_button')
        logoutbutton.clicked.connect(self.train_info_2)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3toM_button')
        logoutbutton.clicked.connect(self.train_menu)

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

    def train_reports(self):
        """Method called when the train reports button is pressed"""
        uic.loadUi('src/UI/TrainModel/Train_Report.ui', self)

        # Find all elements and connect them
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button_report')
        logout_button.clicked.connect(self.logout)

        reports_to_main_button = self.findChild(QtWidgets.QPushButton, 'pageRtoM_button')
        reports_to_main_button.clicked.connect(self.train_menu)

        report_engine_button = self.findChild(QtWidgets.QPushButton, 'report_engine_button')
        report_engine_button.clicked.connect(self.report_engine)

        report_signal_button = self.findChild(QtWidgets.QPushButton, 'report_signal_button')
        report_signal_button.clicked.connect(self.report_signal)

        report_brake_button = self.findChild(QtWidgets.QPushButton, 'report_brake_button')
        report_brake_button.clicked.connect(self.report_brake)

    #######################################################################
    ############################ HELPER METHODS ###########################
    #######################################################################
    def update_current_speed(self):
        responsecode, currentSpeed = send_message(RequestCode.TRAIN_MODEL_UPDATE_CURRENT_SPEED)
    
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
            if value == "":
                self.fail_alert.setText("Some of the parameters are missing")
                self.fail_alert.setStyleSheet("color: red;")
                return
                
            try:
                int(value)
            except ValueError:
                self.fail_alert.setText("All parameters must be integer values")
                self.fail_alert.setStyleSheet("color: red;")
                return

            

        # Send the data to the cloud
        for request_code, value in parameters.items():
            send_message_async(request_code, str(self.current_train_id) + ' ' + value,
                               lambda *args: None)

        self.save_alert.setStyleSheet("color: green;")
        self.fail_alert.setStyleSheet("color: rgb(133, 158, 166);")

    def report_engine(self):
        """Method connected to the report engine failure button"""
        self.alert_sent1.setStyleSheet("color: green;")
        self.alert_sent2.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent3.setStyleSheet("color: rgb(133, 158, 166);")

    def report_signal(self):
        """Method connected to the report signal failure button"""
        self.alert_sent1.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent2.setStyleSheet("color: green;")
        self.alert_sent3.setStyleSheet("color: rgb(133, 158, 166);")

    def report_brake(self):
        """Method connected to the report brake failure button"""
        self.alert_sent1.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent2.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent3.setStyleSheet("color: green;")

    @staticmethod
    def logout(self):
        """Method invoked when the logout button is pressed"""
        if sys.platform == 'darwin':
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
