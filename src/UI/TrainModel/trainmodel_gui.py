"""Train Model GUI"""

import os
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QTimer
import sys

from src.UI.server_functions import send_message_async, RequestCode, send_message, ResponseCode
from src.signals import signals
from src.UI.window_manager import window_list
from src.TrainModel.TrainCatalogue import train_catalogue
from src.TrainModel.BlockCatalogue import block_catalogue

class TrainModelUi(QtWidgets.QMainWindow):
    """UI class for the Train Model"""
    def __init__(self):
        super().__init__()

        # self.train_menu_timer = QTimer()
        # self.train1_info_timer = QTimer()
        # self.train2_info_timer = QTimer()
        # self.train3_info_timer = QTimer()
        # self.train_menu_timer.timeout.connect(self.update_train_list)
        # self.train1_info_timer.timeout.connect(self.update_gui1)
        # self.train2_info_timer.timeout.connect(self.update_gui2)
        # self.train3_info_timer.timeout.connect(self.update_gui3)

        # Receive dispatch train signal and add a train to the drop down
        signals.TRAIN_MODEL_DISPATCH_TRAIN.connect(self.update_train_list)

        # Receive dispatch train signal
        signals.TRAIN_MODEL_DISPATCH_TRAIN.connect(self.train_model_dispatch_train)
        # Receive lights signal
        signals.TRAIN_MODEL_GUI_RECEIVE_LIGHTS.connect(self.train_model_receive_lights)

        self.current_train_id = "1"
        self.train_menu()

    #######################################################################
    ############################## GUI PAGES ##############################
    #######################################################################
    def train_menu(self):
        """Method called after a train is selected"""
        uic.loadUi('src/UI/TrainModel/Train_Menu.ui', self)

        # Update the train drop down
        currentIndex = self.findChild(QtWidgets.QComboBox, 'menu_train_combo').currentIndex()
        self.findChild(QtWidgets.QComboBox, 'menu_train_combo').clear()
        for i in train_catalogue.m_trainList.count():
            self.menu_train_combo.addItem("Train #" + str(i))
        self.findChild(QtWidgets.QComboBox, 'menu_train_combo').setCurrentIndex(currentIndex)

        # self.stop_all_timers() # Restart timers
        # self.train_menu_timer.start(2000)

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

    def update_lights_label(self, light_status):
        print("Here")
        if light_status:
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")

    def update_current_train_id(self):
        self.current_train_id = self.menu_train_combo.currentText()[-1]
        print(self.current_train_id)

    def train_info_1(self):
        # self.stop_all_timers() # Restart timers
        # self.train1_info_timer.start(2000)
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
        # self.stop_all_timers() # Restart timers
        # self.train2_info_timer.start(2000)
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
        # self.stop_all_timers() # Restart timers
        # self.train3_info_timer.start(2000)
        # This is executed when the button is pressed
        uic.loadUi('src/UI/TrainModel/Train_Info_Page3.ui', self)

        signals.lights_toggled.connect(self.update_lights_label)

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
        # self.stop_all_timers() # Restart timers
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
        # self.stop_all_timers() # Restart timers
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

        self.findChild(QtWidgets.QLabel, 'disp_command_speed').setText(str(train_catalogue.m_trainList[self.current_train_id].m_commandSpeed) + " m/s") # Remove trailing zeros from float

        if str(train_catalogue.m_trainList[self.current_train_id].m_authority) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_authority').setText("true")
            self.findChild(QtWidgets.QLabel, 'disp_authority').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_authority').setText("false")
            self.findChild(QtWidgets.QLabel, 'disp_authority').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")

        self.findChild(QtWidgets.QLabel, 'disp_current_speed').setText(str(train_catalogue.m_trainList[self.current_train_id].m_currentSpeed) + " m/s")
        self.findChild(QtWidgets.QLabel, 'disp_speed_limit').setText(str(train_catalogue.m_trainList[self.current_train_id].m_route[0].m_speedLimit) + " km/h")

        if str(train_catalogue.m_trainList[self.current_train_id].m_brakeCommand) == "True":
            self.findChild(QtWidgets.QLabel, 'disp_brake_command').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_brake_command').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_brake_command').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_brake_command').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id].m_serviceBrake) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id].m_emergencyPassengeBrake) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id].m_currentLine) == "0":
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setText("green")
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setText("red")
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            

    def update_gui2(self):
        if "Select Train..." in self.current_train_id:
            return

        # self.findChild(QtWidgets.QLabel, 'disp_acceleration_limit').setText(dataParsed[0].split(".")[0] + " m/s²")
        # self.findChild(QtWidgets.QLabel, 'disp_deceleration_limit').setText(dataParsed[1].split(".")[0] + " m/s²")
        self.findChild(QtWidgets.QLabel, 'disp_acceleration_limit').setText("0.5 m/s²")
        self.findChild(QtWidgets.QLabel, 'disp_deceleration_limit').setText("-1.2 m/s²")

        self.findChild(QtWidgets.QLabel, 'disp_block_elevation').setText(str(train_catalogue.m_trainList[self.current_train_id].m_route[0].m_elevation) + " m")
        self.findChild(QtWidgets.QLabel, 'disp_block_slope').setText(str(train_catalogue.m_trainList[self.current_train_id].m_route[0].m_slope) + " m/s")
        # UPDATE POSITION HERE
        self.findChild(QtWidgets.QLabel, 'disp_block_size').setText(str(train_catalogue.m_trainList[self.current_train_id].m_route[0].m_sizeOfBlock) + " m")
        self.findChild(QtWidgets.QLabel, 'disp_current_block').setText("block #" + str(train_catalogue.m_trainList[self.current_train_id].m_route[0]))
        self.findChild(QtWidgets.QLabel, 'disp_destination_block').setText("block #" + str(train_catalogue.m_trainList[self.current_train_id].m_destinationBlock))

    def update_gui3(self):
        if "Select Train..." in self.current_train_id:
            return

        self.findChild(QtWidgets.QLabel, 'disp_pass_count').setText(str(train_catalogue.m_trainList[self.current_train_id].m_trainPassCount) + " persons")
        self.findChild(QtWidgets.QLabel, 'disp_crew_count').setText(str(train_catalogue.m_trainList[self.current_train_id].m_trainCrewCount) + " persons")

        if str(train_catalogue.m_trainList[self.current_train_id].m_announcements) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id].m_advertisements) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        # print(dataParsed[4]) # TEST PRINT
        if str(train_catalogue.m_trainList[self.current_train_id].m_cabinLights) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id].m_headLights) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        self.findChild(QtWidgets.QLabel, 'disp_temperature_control').setText(str(train_catalogue.m_trainList[self.current_train_id].m_tempControl) + " °F")

        if str(train_catalogue.m_trainList[self.current_train_id].m_doors) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_doors').setText("open")
            self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_doors').setText("closed")
            self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
    
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

    def logout(self):
        """Method invoked when the logout button is pressed"""
        window_list.remove(self)

    # def stop_all_timers(self):
    #     self.train_menu_timer.stop()
    #     self.train1_info_timer.stop()
    #     self.train2_info_timer.stop()
    #     self.train3_info_timer.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModelUi()
    app.exec_()
