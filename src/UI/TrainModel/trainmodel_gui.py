"""Train Model GUI"""

import os
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QTimer
import sys

sys.path.insert(1, 'src')
from UI.server_functions import send_message_async, RequestCode, send_message, ResponseCode

class Ui(QtWidgets.QMainWindow):
    """UI class for the Train Model"""
    def __init__(self):
        super(Ui, self).__init__()

        self.train_menu_timer = QTimer()
        self.train1_info_timer = QTimer()
        self.train2_info_timer = QTimer()
        self.train3_info_timer = QTimer()
        self.train_menu_timer.timeout.connect(self.update_train_list)
        self.train1_info_timer.timeout.connect(self.update_gui1)
        self.train2_info_timer.timeout.connect(self.update_gui2)
        self.train3_info_timer.timeout.connect(self.update_gui3)

        self.current_train_id = "1"
        self.train_menu()

    #######################################################################
    ############################## GUI PAGES ##############################
    #######################################################################
    def train_menu(self):
        """Method called after a train is selected"""
        uic.loadUi('src/UI/TrainModel/Train_Menu.ui', self)

        self.stop_all_timers() # Restart timers
        self.train_menu_timer.start(2000)

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
        self.menu_train_combo.currentIndexChanged.connect(self.update_current_train_id)
        train_info_button.clicked.connect(self.train_info_1)

        train_parameters_button = self.findChild(QtWidgets.QPushButton, 'train_parameters_button')
        train_parameters_button.clicked.connect(self.train_parameters)

        train_reports_button = self.findChild(QtWidgets.QPushButton, 'train_reports_button')
        train_reports_button.clicked.connect(self.train_reports)

        # Show the page
        self.show()

    def update_current_train_id(self):
        self.current_train_id = self.menu_train_combo.currentText()[-1]
        print(self.current_train_id)

    def train_info_1(self):
        self.stop_all_timers() # Restart timers
        self.train1_info_timer.start(2000)
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page1.ui', self)

        # Update Label page1_train_label
        if "Select Train..." not in self.current_train_id:
            self.findChild(QtWidgets.QLabel, 'page1_train_label').setText("Train #" + self.current_train_id + " Info")

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
        self.stop_all_timers() # Restart timers
        self.train2_info_timer.start(2000)
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page2.ui', self)

        # Update Label page2_train_label
        if "Select Train..." not in self.current_train_id:
            self.findChild(QtWidgets.QLabel, 'page2_train_label').setText("Train #" + self.current_train_id + " Info")
        
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
        self.stop_all_timers() # Restart timers
        self.train3_info_timer.start(2000)
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page3.ui', self)

        # Update Label page3_train_label
        if "Select Train..." not in self.current_train_id:
            self.findChild(QtWidgets.QLabel, 'page3_train_label').setText("Train #" + self.current_train_id + " Info")
        
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info3')
        logoutbutton.clicked.connect(self.logout)

        button = self.findChild(QtWidgets.QPushButton, 'report_button_info3')
        button.clicked.connect(self.train_reports)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3to2_button')
        logoutbutton.clicked.connect(self.train_info_2)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3toM_button')
        logoutbutton.clicked.connect(self.train_menu)

    def train_parameters(self):
        self.stop_all_timers() # Restart timers
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
        self.stop_all_timers() # Restart timers
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

    # ADD CURRENT PAGE VARIABLE
    def update_gui1(self):
        if "Select Train..." in self.current_train_id:
            return
        responsecode, dataReceived = send_message(RequestCode.TRAIN_MODEL_GUI_1_GATHER_DATA, str(self.current_train_id))
        if responsecode == ResponseCode.SUCCESS:
            # Parse the data and update the gui.
            dataParsed = dataReceived.split()
            self.findChild(QtWidgets.QLabel, 'disp_command_speed').setText(dataParsed[0] + " m/s")

            if dataParsed[1] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_authority').setText("true")
                self.findChild(QtWidgets.QLabel, 'disp_authority').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_authority').setText("false")
                self.findChild(QtWidgets.QLabel, 'disp_authority').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")

            self.findChild(QtWidgets.QLabel, 'disp_current_speed').setText(dataParsed[2] + " m/s")
            self.findChild(QtWidgets.QLabel, 'disp_speed_limit').setText(dataParsed[3] + " km/h")

            if dataParsed[4] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_brake_command').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_brake_command').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_brake_command').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_brake_command').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            
            if dataParsed[5] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_service_brake').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_service_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_service_brake').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_service_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            
            if dataParsed[6] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            
            if dataParsed[7] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_current_line').setText("green")
                self.findChild(QtWidgets.QLabel, 'disp_current_line').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_current_line').setText("red")
                self.findChild(QtWidgets.QLabel, 'disp_current_line').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            

    def update_gui2(self):
        if "Select Train..." in self.current_train_id:
            return
        responsecode, dataReceived = send_message(RequestCode.TRAIN_MODEL_GUI_2_GATHER_DATA, str(self.current_train_id))
        if responsecode == ResponseCode.SUCCESS:
            # Parse the data and update the gui.
            dataParsed = dataReceived.split()
            self.findChild(QtWidgets.QLabel, 'disp_acceleration_limit').setText(dataParsed[0] + " m/s²")
            self.findChild(QtWidgets.QLabel, 'disp_deceleration_limit').setText(dataParsed[1] + " m/s²")
            self.findChild(QtWidgets.QLabel, 'disp_block_elevation').setText(dataParsed[2] + " m")
            self.findChild(QtWidgets.QLabel, 'disp_block_slope').setText(dataParsed[3] + " m/s")
            # UPDATE POSITION HERE
            self.findChild(QtWidgets.QLabel, 'disp_block_size').setText(dataParsed[4] + " m")
            self.findChild(QtWidgets.QLabel, 'disp_current_block').setText("block #" + dataParsed[5])
            self.findChild(QtWidgets.QLabel, 'disp_destination_block').setText("block #" + dataParsed[6])

    def update_gui3(self):
        if "Select Train..." in self.current_train_id:
            return
        responsecode, dataReceived = send_message(RequestCode.TRAIN_MODEL_GUI_3_GATHER_DATA, str(self.current_train_id))
        if responsecode == ResponseCode.SUCCESS:
            # Parse the data and update the gui.
            dataParsed = dataReceived.split()
            self.findChild(QtWidgets.QLabel, 'disp_pass_count').setText(dataParsed[0] + " persons")
            self.findChild(QtWidgets.QLabel, 'disp_crew_count').setText(dataParsed[1] + " persons")

            if dataParsed[2] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_announcements').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_announcements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_announcements').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_announcements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            
            if dataParsed[3] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_advertisements').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_advertisements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_advertisements').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_advertisements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            print(dataParsed[4]) # TEST PRINT
            if dataParsed[4] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            
            if dataParsed[5] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_head_lights').setText("on")
                self.findChild(QtWidgets.QLabel, 'disp_head_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_head_lights').setText("off")
                self.findChild(QtWidgets.QLabel, 'disp_head_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            
            self.findChild(QtWidgets.QLabel, 'disp_temperature_control').setText(dataParsed[6] + " persons")

            if dataParsed[7] == 1:
                self.findChild(QtWidgets.QLabel, 'disp_doors').setText("open")
                self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_doors').setText("closed")
                self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            

    def update_train_list(self):
        responsecode, dataReceived = send_message(RequestCode.TRAIN_MODEL_GUI_UPDATE_DROP_DOWN)
        if responsecode == ResponseCode.SUCCESS:
            # Parse the data and update the gui.
            dataParsed = int(dataReceived)
            count = 1
            currentIndex = self.findChild(QtWidgets.QComboBox, 'menu_train_combo').currentIndex()
            #self.menu_train_combo.clear()
            self.findChild(QtWidgets.QComboBox, 'menu_train_combo').clear()
            while(count < dataParsed + 1):
                self.menu_train_combo.addItem("Train #" + str(count))
                count = count + 1
            self.findChild(QtWidgets.QComboBox, 'menu_train_combo').setCurrentIndex(currentIndex)
    
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

    def stop_all_timers(self):
        self.train_menu_timer.stop()
        self.train1_info_timer.stop()
        self.train2_info_timer.stop()
        self.train3_info_timer.stop()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
