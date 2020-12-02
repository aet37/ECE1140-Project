"""Train Model GUI"""

from enum import Enum
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QTimer
import sys
sys.path.append(".")

from src.signals import signals
from src.UI.window_manager import window_list
from src.TrainModel.TrainCatalogue import train_catalogue
from src.TrainModel.BlockCatalogue import block_catalogue_green, block_catalogue_red
from src.UI.Common.common import Alert
from src.common_def import *

class Page(Enum):
    MENU = 0
    INFO_1 = 1
    INFO_2 = 2
    INFO_3 = 3
    PARAMETERS = 4
    REPORTS = 5

class TrainModelUi(QtWidgets.QMainWindow):
    """UI class for the Train Model"""
    def __init__(self):
        super().__init__()

        # Receive a change
        signals.train_model_something_has_been_changed.connect(self.update_current_page)
        signals.train_model_dropdown_has_been_changed.connect(self.update_dropdown)

        # Current train id that's selected in the drop down menu
        self.current_train_id = 0

        # Current page that's being displayed
        self.current_page = Page.MENU

        self.testDispTrainCount = 1

        # Start by displaying the train menu page
        self.train_menu()

        # Show the page
        self.show()

    def train_menu(self):
        """Method called after a train is selected"""
        uic.loadUi('src/UI/TrainModel/Train_Menu.ui', self)
        self.current_page = Page.MENU

        # Update the dropdown accordingly
        self.update_dropdown()

        # Find all elements and connect them accordingly
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button_menu')
        logout_button.clicked.connect(self.logout)

        train_info_button = self.findChild(QtWidgets.QPushButton, 'train_info_button')
        self.menu_train_combo.currentIndexChanged.connect(self.update_current_train_id)
        train_info_button.clicked.connect(self.train_info_1)

        train_reports_button = self.findChild(QtWidgets.QPushButton, 'train_reports_button')
        train_reports_button.clicked.connect(self.train_reports)

    def update_current_train_id(self):
        """Updates the current train id with what's selected"""
        if "Select Train..." in self.menu_train_combo.currentText():
            self.current_train_id = 0
        else:
            self.current_train_id = int(self.menu_train_combo.currentText().split('#')[1])

    def train_info_1(self):
        """This is executed when the button is pressed"""
        # Block the user from reaching this page without a train selected
        if self.current_train_id == 0:
            alert = Alert("Please select a train from the drop down menu")
            alert.exec_()
            return

        uic.loadUi('src/UI/TrainModel/Train_Info_Page1.ui', self)
        self.current_page = Page.INFO_1

        # Update Label page1_train_label
        self.findChild(QtWidgets.QLabel, 'page1_train_label').setText("Train #{} Info".format(self.current_train_id))

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
        self.current_page = Page.INFO_2

        # Update Label page2_train_label
        self.findChild(QtWidgets.QLabel, 'page2_train_label').setText("Train #{} Info".format(self.current_train_id))
        
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
        self.current_page = Page.INFO_3

        # Update Label page3_train_label
        self.findChild(QtWidgets.QLabel, 'page3_train_label').setText("Train #{} Info".format(self.current_train_id))
        
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'logout_button_info3')
        logoutbutton.clicked.connect(self.logout)

        button = self.findChild(QtWidgets.QPushButton, 'report_button_info3')
        button.clicked.connect(self.train_reports)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3to2_button')
        logoutbutton.clicked.connect(self.train_info_2)
        logoutbutton = self.findChild(QtWidgets.QPushButton, 'page3toM_button')
        logoutbutton.clicked.connect(self.train_menu)

    def train_reports(self):
        """Method called when the train reports button is pressed"""
        # Block the user from reaching this page without a train selected
        if self.current_train_id == 0:
            alert = Alert("Please select a train from the drop down menu")
            alert.exec_()
            return
        
        uic.loadUi('src/UI/TrainModel/Train_Report.ui', self)
        self.current_page = Page.REPORTS

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

        murphy_ebrake_button = self.findChild(QtWidgets.QPushButton, 'murphy_ebrake')
        murphy_ebrake_button.clicked.connect(self.murphy_ebrake_pull)

    #######################################################################
    ############################ HELPER METHODS ###########################
    ####################################################################### "{:.2f} MPH".format(str(train_catalogue.m_trainList[self.current_train_id - 1].m_commandSpeed))

    def update_gui1(self):
        self.findChild(QtWidgets.QLabel, 'disp_command_speed').setText("{:.2f} MPH".format(train_catalogue.m_trainList[self.current_train_id - 1].m_commandSpeed)) # Remove trailing zeros from float

        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_authority) == "1":
            self.findChild(QtWidgets.QLabel, 'disp_authority').setText("true")
            self.findChild(QtWidgets.QLabel, 'disp_authority').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_authority').setText("false")
            self.findChild(QtWidgets.QLabel, 'disp_authority').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")

        self.findChild(QtWidgets.QLabel, 'disp_current_speed').setText("{:.2f} MPH".format(train_catalogue.m_trainList[self.current_train_id - 1].m_currentSpeed))
        
        if len(train_catalogue.m_trainList[self.current_train_id - 1].m_route) == 0:
            self.findChild(QtWidgets.QLabel, 'disp_speed_limit').setText(str(0.0) + " km/h")
        else:
            if train_catalogue.m_trainList[self.current_train_id - 1].m_currentLine == Line.LINE_GREEN:
                self.findChild(QtWidgets.QLabel, 'disp_speed_limit').setText(str(block_catalogue_green.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_speedLimit) + " km/h")
            else:
                self.findChild(QtWidgets.QLabel, 'disp_speed_limit').setText(str(block_catalogue_red.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_speedLimit) + " km/h")
        
        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_serviceBrake) == "True":
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_service_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_emergencyPassengerBrake) == "True":
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_emergency_passenger_brake').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if train_catalogue.m_trainList[self.current_train_id - 1].m_currentLine == Line.LINE_GREEN:
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setText("green")
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setText("red")
            self.findChild(QtWidgets.QLabel, 'disp_current_line').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
            

    def update_gui2(self):
        # self.findChild(QtWidgets.QLabel, 'disp_acceleration_limit').setText(dataParsed[0].split(".")[0] + " m/s²")
        # self.findChild(QtWidgets.QLabel, 'disp_deceleration_limit').setText(dataParsed[1].split(".")[0] + " m/s²")
        self.findChild(QtWidgets.QLabel, 'disp_acceleration_limit').setText("0.5 m/s²")
        self.findChild(QtWidgets.QLabel, 'disp_deceleration_limit').setText("-1.2 m/s²")
        block_catalogue_green.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_elevation
        if train_catalogue.m_trainList[self.current_train_id - 1].m_currentLine == Line.LINE_GREEN:
            self.findChild(QtWidgets.QLabel, 'disp_block_elevation').setText(str(block_catalogue_green.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_elevation) + " m")
            self.findChild(QtWidgets.QLabel, 'disp_block_slope').setText(str(block_catalogue_green.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_slope) + " m/s")
            self.findChild(QtWidgets.QLabel, 'disp_block_size').setText(str(block_catalogue_green.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_sizeOfBlock) + " m")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_block_elevation').setText(str(block_catalogue_red.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_elevation) + " m")
            self.findChild(QtWidgets.QLabel, 'disp_block_slope').setText(str(block_catalogue_red.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_slope) + " m/s")
            self.findChild(QtWidgets.QLabel, 'disp_block_size').setText(str(block_catalogue_red.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].m_sizeOfBlock) + " m")
        
        self.findChild(QtWidgets.QLabel, 'disp_position').setText("{:.2f} m".format(train_catalogue.m_trainList[self.current_train_id - 1].m_position))
        self.findChild(QtWidgets.QLabel, 'disp_current_block').setText("block #" + str(train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]))
        self.findChild(QtWidgets.QLabel, 'disp_destination_block').setText("block #" + str(train_catalogue.m_trainList[self.current_train_id - 1].m_destinationBlock))

    def update_gui3(self):
        self.findChild(QtWidgets.QLabel, 'disp_pass_count').setText(str(train_catalogue.m_trainList[self.current_train_id - 1].m_trainPassCount) + " persons")
        self.findChild(QtWidgets.QLabel, 'disp_crew_count').setText(str(train_catalogue.m_trainList[self.current_train_id - 1].m_trainCrewCount) + " persons")

        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_announcements) == "True":
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setText("Station: " + str(block_catalogue_green.m_blockList[train_catalogue.m_trainList[self.current_train_id - 1].m_route[0]].beacon1.station_name))
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_announcements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_advertisements) == "True":
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_advertisements').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        # print(dataParsed[4]) # TEST PRINT
        # print("Are you HeRe?" + str(train_catalogue.m_trainList[self.current_train_id - 1].m_cabinLights))  
        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_cabinLights) == "True":
            # print("Are you in the lights?")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_cabin_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_headLights) == "True":
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setText("on")
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setText("off")
            self.findChild(QtWidgets.QLabel, 'disp_head_lights').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
        
        self.findChild(QtWidgets.QLabel, 'disp_temperature_control').setText(str(train_catalogue.m_trainList[self.current_train_id - 1].m_tempControl) + " °F")

        if str(train_catalogue.m_trainList[self.current_train_id - 1].m_doors) == "True" and train_catalogue.m_trainList[self.current_train_id - 1].m_doorSide == DoorSide.SIDE_RIGHT:
            self.findChild(QtWidgets.QLabel, 'disp_doors').setText("right side doors")
            self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        elif str(train_catalogue.m_trainList[self.current_train_id - 1].m_doors) == "True" and train_catalogue.m_trainList[self.current_train_id - 1].m_doorSide == DoorSide.SIDE_LEFT:
            self.findChild(QtWidgets.QLabel, 'disp_doors').setText("left side doors")
            self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        elif str(train_catalogue.m_trainList[self.current_train_id - 1].m_doors) == "True" and train_catalogue.m_trainList[self.current_train_id - 1].m_doorSide == DoorSide.SIDE_BOTH:
            self.findChild(QtWidgets.QLabel, 'disp_doors').setText("both side doors")
            self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(26, 171, 0);")
        else:
            self.findChild(QtWidgets.QLabel, 'disp_doors').setText("closed")
            self.findChild(QtWidgets.QLabel, 'disp_doors').setStyleSheet("background-color: rgba(255, 255, 255, 0);\ncolor: rgb(220, 44, 44);")
    
    def update_dropdown(self):
        """
        This will update the dropdown when a train is dispatched
        """
        if self.current_page == Page.MENU:
            # Update the train drop down
            currentIndex = self.findChild(QtWidgets.QComboBox, 'menu_train_combo').currentIndex()
            self.findChild(QtWidgets.QComboBox, 'menu_train_combo').clear()
            for i in range(0, len(train_catalogue.m_trainList)):
                self.menu_train_combo.addItem("Train #" + str(i + 1))
            self.findChild(QtWidgets.QComboBox, 'menu_train_combo').setCurrentIndex(currentIndex)
            self.update_current_train_id()

    def update_current_page(self):
        """
        This will update the current page that we are on
        """
        
        # if self.current_page == Page.MENU:
        #     self.update_dropdown()
        # elif self.current_page == Page.INFO_1:
        #     self.update_gui1()
        if self.current_page == Page.INFO_1:
            self.update_gui1()
        elif self.current_page == Page.INFO_2:
            self.update_gui2()
        elif self.current_page == Page.INFO_3:
            self.update_gui3()
        else:
            return

    def report_engine(self):
        """Method connected to the report engine failure button"""
        signals.train_model_report_e_failure.emit(self.current_train_id - 1, True)
        self.alert_sent1.setStyleSheet("color: green;")
        self.alert_sent2.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent3.setStyleSheet("color: rgb(133, 158, 166);")

    def report_signal(self):
        """Method connected to the report signal failure button"""
        signals.train_model_report_sp_failure.emit(self.current_train_id - 1, True)
        self.alert_sent1.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent2.setStyleSheet("color: green;")
        self.alert_sent3.setStyleSheet("color: rgb(133, 158, 166);")

    def report_brake(self):
        """Method connected to the report brake failure button"""
        signals.train_model_report_sb_failure.emit(self.current_train_id - 1, True)
        signals.swtrain_receive_brake_failure.emit(self.current_train_id - 1, True)
        self.alert_sent1.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent2.setStyleSheet("color: rgb(133, 158, 166);")
        self.alert_sent3.setStyleSheet("color: green;")

    def murphy_ebrake_pull(self):
        signals.train_model_gui_receive_ebrake.emit(self.current_train_id - 1, True)

    def logout(self):
        """Method invoked when the logout button is pressed"""
        # signals.train_model_dispatch_train.emit(self.testDispTrainCount, 0, 0, 0, 0)
        # self.testDispTrainCount += 1
        window_list.remove(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModelUi()
    app.exec_()
