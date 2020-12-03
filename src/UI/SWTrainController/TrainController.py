import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
sys.path.append(".")
from src.UI.Common.common import Alert, Confirmation

from src.signals import signals
from src.UI.window_manager import window_list
# Import singleton instance of control system
from src.SWTrainController.ControlSystem import control_system
from src.common_def import Converters

from src.logger import get_logger

logger = get_logger(__name__)

class SWTrainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Define current train id
        self.current_train_id = "1"
        # Define amount of trains
        self.controller_count = 0

        uic.loadUi('src/UI/SWTrainController/TrainController.ui', self)

        self.TrainIDBox.currentIndexChanged.connect(self.update_current_train_id) # Dropdown box
        self.TrainIDBox2.currentIndexChanged.connect(self.update_current_train_id2) # Dropdown box
        self.TrainIDBox3.currentIndexChanged.connect(self.update_current_train_id3) # Dropdown box
        self.TrainIDBox4.currentIndexChanged.connect(self.update_current_train_id4) # Dropdown box

        # Initialize all buttons and the page of the UI
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.stacked_widget.setCurrentIndex(0)

        # Define buttons on main page #
        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.engineer_page.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        ########################################

        # Define buttons on Train Actions page #
        # When doors button is clicked, go to toggle_doors function
        self.doors_button.clicked.connect(self.toggle_doors)

        # When light button is clicked, go to toggle_lights function
        self.lights_button.clicked.connect(self.toggle_lights)

        # When announcements button is clicked, go to toggle_announcements function
        self.announcements_button.clicked.connect(self.toggle_announcements)

        # When advertisements button is clicked go to toggle_ads function
        self.advertisements_button.clicked.connect(self.toggle_ads)

        # When temperature button is clicked go to set_sean_paul function
        self.sean_paul_buttton.clicked.connect(self.set_sean_paul)

        # When User wants to toggle mode, go to toggle_mode function
        self.automatic_mode.clicked.connect(self.toggle_mode1)
        self.manual_mode.clicked.connect(self.toggle_mode2)

        # When set setpoint button is clicked, go to set_setpoint function
        self.set_setpoint_speed.clicked.connect(self.set_setpoint)

        # When service brake button is clicked, go to toggle_service_brake function
        self.service_brake.clicked.connect(self.toggle_service_brake)

        # When emergency brake button is clicked, go to toggle_emergency_brake function
        self.emergency_brake.clicked.connect(self.toggle_emergency_brake)
        ##########################################

        # Define buttons on Failures page ########
        self.brake_failure.clicked.connect(self.resolve_brake_failure)
        ##########################################

        # Define buttons on Engineer page #
        self.save_kp_ki.clicked.connect(self.save_inputs)
        self.use_default_kp_ki.clicked.connect(self.use_defaults)
        ###################################

        # Define Signal Connections #
        signals.swtrain_dispatch_train.connect(self.update_controller_list)
        signals.train_model_receive_power.connect(self.update_gui)
        signals.swtrain_update_current_speed.connect(self.update_gui)
        signals.swtrain_update_authority.connect(self.update_gui)
        signals.swtrain_update_command_speed.connect(self.update_gui)

        # Update controllers if received before opening
        for _ in range(0, len(control_system.p_controllers) ):
            self.update_controller_list()

        # Define function so comboboxes change synchronously #
        self.TrainIDBox.currentIndexChanged.connect(self.update_dropdowns)
        self.TrainIDBox2.currentIndexChanged.connect(self.update_dropdowns)
        self.TrainIDBox3.currentIndexChanged.connect(self.update_dropdowns)
        self.TrainIDBox4.currentIndexChanged.connect(self.update_dropdowns)

        # Define main menu buttons #
        self.return_button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.return_button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.return_button3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        ############################

        # Define logout buttons #
        self.logout_button = self.findChild(QtWidgets.QPushButton, 'Logout') # Find the button
        self.logout_button.clicked.connect(self.logout)
        self.logout_button2 = self.findChild(QtWidgets.QPushButton, 'Logout2') # Find the button
        self.logout_button2.clicked.connect(self.logout)
        self.logout_button3 = self.findChild(QtWidgets.QPushButton, 'Logout3') # Find the button
        self.logout_button3.clicked.connect(self.logout)
        self.logout_button4 = self.findChild(QtWidgets.QPushButton, 'Logout4')
        self.logout_button4.clicked.connect(self.logout)
        ###########################

        self.show()

    # Initialize buttons in UI
    def initUI(self):
        # Define buttons on main page #
        self.button1 = self.findChild(QtWidgets.QPushButton, 'TrainActions') # Find the button
        self.button2 = self.findChild(QtWidgets.QPushButton, 'Information') # Find the button
        self.engineer_page = self.findChild(QtWidgets.QPushButton, 'TrainEngineer')
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget') # Find stacked widget
        ########################################

        # Define buttons on Train Actions Page #
        self.return_button1 = self.findChild(QtWidgets.QPushButton, 'MainMenu2')

        # Define button for doors
        self.doors_button = self.findChild(QtWidgets.QPushButton, 'Doors')

        # Define button for lights
        self.lights_button = self.findChild(QtWidgets.QPushButton, 'Lights')

        # Define button for announcements
        self.announcements_button = self.findChild(QtWidgets.QPushButton, 'Announcements')

        # Define button for advertisements
        self.advertisements_button = self.findChild(QtWidgets.QPushButton, 'Advertisements')

        # Define button for setting temperature
        self.sean_paul_buttton = self.findChild(QtWidgets.QPushButton, 'SeanPaul')

        # Define Automatic Mode button
        self.automatic_mode = self.findChild(QtWidgets.QPushButton, 'AutomaticMode')
        # Define Manual Mode button
        self.manual_mode = self.findChild(QtWidgets.QPushButton, 'ManualMode')

        # Define set speed button
        self.set_setpoint_speed = self.findChild(QtWidgets.QPushButton, 'SetSpeed')

        # Define service brake button
        self.service_brake = self.findChild(QtWidgets.QPushButton, 'ServiceBrake')

        # Define emergency brake button
        self.emergency_brake = self.findChild(QtWidgets.QPushButton, 'EmergencyBrake')
        ###################################

        # Define buttons on Information Page #
        self.return_button2 = self.findChild(QtWidgets.QPushButton, 'MainMenu3')

        # Define brake failure button
        self.brake_failure = self.findChild(QtWidgets.QPushButton, 'brake_failure')
        # Define brake failure status
        self.brake_failure_status = self.findChild(QtWidgets.QTextBrowser, 'brake_failure_status')

        # Define engine failure button
        self.engine_failure = self.findChild(QtWidgets.QPushButton, 'engine_failure')
        # Define engine failure status
        self.engine_failure_status = self.findChild(QtWidgets.QTextBrowser, 'engine_failure_status')

        # Define signal pickup failure button
        self.signal_pickup_failure = self.findChild(QtWidgets.QPushButton, 'signal_pickup_failure')
        # Define engine failure status
        self.signal_pickup_status = self.findChild(QtWidgets.QTextBrowser, 'signal_pickup_status')
        ###################################

        # Define buttons on Engineer Page #
        self.return_button3 = self.findChild(QtWidgets.QPushButton, 'MainMenu4')

        # Define button to input Kp and Ki
        self.save_kp_ki = self.findChild(QtWidgets.QPushButton, 'SaveInputs')

        # Define button to input Default Kp and Ki values
        self.use_default_kp_ki = self.findChild(QtWidgets.QPushButton, 'UseDefaults')
        ##################################

    def update_current_train_id(self):
        self.current_train_id = self.TrainIDBox.currentText()

    def update_current_train_id2(self):
        self.current_train_id = self.TrainIDBox2.currentText()

    def update_current_train_id3(self):
        self.current_train_id = self.TrainIDBox3.currentText()

    def update_current_train_id4(self):
        self.current_train_id = self.TrainIDBox4.currentText()

    def update_controller_list(self):
        logger.info("Updating controller list")
        # Whenever the swtrain_dispatch_train signal is called, add another controller to list
        self.controller_count += 1
        self.TrainIDBox.addItem(str(self.controller_count))
        self.TrainIDBox2.addItem(str(self.controller_count))
        self.TrainIDBox3.addItem(str(self.controller_count))
        self.TrainIDBox4.addItem(str(self.controller_count))

    def update_dropdowns(self):
        # Find current index of all dropdowns
        currentIndex = self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentIndex()
        currentIndex2 = self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').currentIndex()
        currentIndex3 = self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').currentIndex()
        currentIndex4 = self.findChild(QtWidgets.QComboBox, 'TrainIDBox4').currentIndex()

        # Update all dropdowns depending on which page is up
        if self.stacked_widget.currentIndex() == 0:
            self.update_current_train_id()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox4').setCurrentIndex(currentIndex)
        elif self.stacked_widget.currentIndex() == 1:
            self.update_current_train_id2()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex2)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex2)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex2)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox4').setCurrentIndex(currentIndex2)
        elif self.stacked_widget.currentIndex() == 2:
            self.update_current_train_id3()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex3)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex3)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex3)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox4').setCurrentIndex(currentIndex3)
        else:
            self.update_current_train_id4()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex4)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex4)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex4)
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox4').setCurrentIndex(currentIndex4)

        # Update GUI data when new dropdown item is chosen
        self.update_gui()

    def update_gui(self):
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            return

        # Store all data into individual variables
        self.doors_status = control_system.p_controllers[int(self.current_train_id) - 1].doors
        self.lights_status = control_system.p_controllers[int(self.current_train_id) - 1].lights
        self.announcements_status = control_system.p_controllers[int(self.current_train_id) - 1].announcements
        self.advertisements_status = control_system.p_controllers[int(self.current_train_id) - 1].advertisements
        self.curr_speed = control_system.p_controllers[int(self.current_train_id) - 1].current_speed
        self.com_speed = control_system.p_controllers[int(self.current_train_id) - 1].command_speed * Converters.KmHr_to_MPH
        self.setpoint_speed = control_system.p_controllers[int(self.current_train_id) - 1].setpoint_speed
        self.service_brake_status = control_system.p_controllers[int(self.current_train_id) - 1].service_brake
        self.emergency_brake_status = control_system.p_controllers[int(self.current_train_id) - 1].emergency_brake
        self.mode_status = control_system.p_controllers[int(self.current_train_id) - 1].mode
        self.kp_status = control_system.p_controllers[int(self.current_train_id) - 1].kp
        self.ki_status = control_system.p_controllers[int(self.current_train_id) - 1].ki
        self.power_status = control_system.p_controllers[int(self.current_train_id) - 1].power_command
        self.authority_status = control_system.p_controllers[int(self.current_train_id) - 1].authority
        self.brake_fail_status = control_system.p_controllers[int(self.current_train_id) - 1].brake_failure
        self.engine_fail_status = control_system.p_controllers[int(self.current_train_id) - 1].engine_failure
        self.signal_fail_status = control_system.p_controllers[int(self.current_train_id) - 1].signal_pickup_failure

        # Change GUI to reflect current data
        # Update doors
        if self.doors_status == 1:
            self.doors_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.doors_button.setStyleSheet("background-color: green;")

        # Update lights
        if self.lights_status == 1:
            self.lights_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.lights_button.setStyleSheet("background-color: green;")

        # Update announcements
        if self.announcements_status == 1:
            self.announcements_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.announcements_button.setStyleSheet("background-color: green;")

        # Update advertisements
        if self.advertisements_status == 1:
            self.advertisements_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.advertisements_button.setStyleSheet("background-color: green;")

        # Update current speed
        self.current_speed_label.setText("{:.2f} MPH".format(self.curr_speed))

        # Update command speed
        self.command_speed_label.setText("{:.2f} MPH".format(self.com_speed))

        # Update setpoint speed
        self.setpoint_speed_label.setText("{:.2f} MPH".format(self.setpoint_speed))

        # Update power
        self.power_command_label.setText("{:.2f} W".format(self.power_status))

        # Update authority
        self.authority_label.setText(str(self.authority_status))

        # Update service brake
        if self.service_brake_status == 1:
            self.service_brake.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.service_brake.setStyleSheet("background-color: green;")

        # Update emergency brake
        if self.emergency_brake_status == 1:
            self.emergency_brake.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.emergency_brake.setStyleSheet("background-color: green;")

        # Update mode buttons
        if self.mode_status == 1:
            self.automatic_mode.setStyleSheet("background-color: rgb(255, 51, 16);")
            self.manual_mode.setStyleSheet("background-color: green;")
        else:
            self.automatic_mode.setStyleSheet("background-color: green;")
            self.manual_mode.setStyleSheet("background-color: rgb(255, 51, 16);")

        # Update failure boxes
        if self.brake_fail_status == True and self.curr_speed == 0 and self.service_brake_status == 1:
            self.brake_failure_status.setStyleSheet("background-color: rgb(255, 51, 16);")
            #alert = Alert("ALERT: A BRAKE FAILURE HAS OCCURRED!")
            #alert.exec_()
        else:
            self.brake_failure_status.setStyleSheet("background-color: green;")

        # Update Kp and Ki
        self.KpLabel.setText(str(self.kp_status) + " W/(m/s)")
        self.KiLabel.setText(str(self.ki_status) + " W/m")


    def set_button_state(self, index):
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.return_button1.setEnabled(True)
        self.return_button2.setEnabled(True)

    def toggle_lights(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Tell train to toggle lights
        signals.swtrain_gui_toggle_cabin_lights.emit(int(self.current_train_id) - 1)

        # Toggle light button color
        if self.lights_button.styleSheet() == "background-color: green;":
            self.lights_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.lights_button.setStyleSheet("background-color: green;")

    def toggle_doors(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Tell train to toggle doors
        signals.swtrain_gui_toggle_damn_doors.emit(int(self.current_train_id) - 1)

        # Toggle door button color
        if self.doors_button.styleSheet() == "background-color: green;":
            self.doors_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.doors_button.setStyleSheet("background-color: green;")

    def toggle_announcements(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Tell train to toggle announcements
        signals.swtrain_gui_announce_stations.emit(int(self.current_train_id) - 1)

        # Toggle announcement button color
        if self.announcements_button.styleSheet() == "background-color: green;":
            self.announcements_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.announcements_button.setStyleSheet("background-color: green;")

    def toggle_ads(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Tell train to toggle advertisements
        signals.swtrain_gui_display_ads.emit(int(self.current_train_id) - 1)

        # Toggle advertisement button color
        if self.advertisements_button.styleSheet() == "background-color: green;":
            self.advertisements_button.setStyleSheet("background-color: rgb(255, 51, 16);")
        else:
            self.advertisements_button.setStyleSheet("background-color: green;")

    def set_sean_paul(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        temp = self.findChild(QtWidgets.QLineEdit, "InputTemp").text()
        try:
            float(temp)
        except ValueError:
            alert = Alert("Temperature must be an numeric value")
            alert.exec_()
            return

        if float(temp) < 64 or float(temp) > 80 :
            alert = Alert("Invalid temperature!")
            alert.exec_()
            return

        # Send alert to notify if temperature was set correctly
        alert = Alert("Temperature set: " + str(temp) + "°F")
        alert.exec_()

        # If input temperature is valid, emit signal
        signals.swtrain_gui_set_sean_paul.emit( (int(self.current_train_id) - 1), float(temp) )

    def toggle_mode1(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # If automatic mode is green, button does nothing
        if self.automatic_mode.styleSheet() == "background-color: green;" :
            return

        # Get attempted override code
        override = self.findChild(QtWidgets.QLineEdit, "OverrideCode").text()

        # Check if override code is correct
        if override != "override" :
            alert = Alert("Invalid override code!")
            alert.exec_()
            return
        else: #Case if override code is correct, confirm choice
            confirmation = Confirmation("Code is correct!\nSwitch mode to Automatic?")
            response = confirmation.exec_()
            if response == False:
                return
            else:
                # Toggle color of mode boxes
                self.automatic_mode.setStyleSheet("background-color: green;")
                self.manual_mode.setStyleSheet("background-color: rgb(255, 51, 16);")

        # Clear override code text boxes
        self.OverrideCode.clear()

        signals.swtrain_gui_switch_mode.emit(int(self.current_train_id) - 1, override)

    def toggle_mode2(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # If manual mode is green, button does nothing
        if self.manual_mode.styleSheet() == "background-color: green;":
            return

        # Get attempted override code
        override = self.findChild(QtWidgets.QLineEdit, "OverrideCode").text()

        # Check if override code is correct
        if override != "override" :
            alert = Alert("Invalid override code!")
            alert.exec_()
            return
        else: #Case if override code is correct, confirm choice
            confirmation = Confirmation("Code is correct!\nSwitch mode to Manual?")
            response = confirmation.exec_()
            if response == False:
                return
            else:
                # Toggle color of mode boxes
                self.automatic_mode.setStyleSheet("background-color: rgb(255, 51, 16);")
                self.manual_mode.setStyleSheet("background-color: green;")

        # Clear override code text boxes
        self.OverrideCode.clear()

        signals.swtrain_gui_switch_mode.emit(int(self.current_train_id) - 1, override)

    def set_setpoint(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Get setpoint speed
        setpoint_speed = self.findChild(QtWidgets.QLineEdit, "EnterSpeed").text()
        setpoint_speed = setpoint_speed.split()[0]
        # Check if number was entered
        try:
            float(setpoint_speed)
        except ValueError:
            alert = Alert("Setpoint speed must be an integer value")
            alert.exec_()
            return

        # Check if speed entered is within valid range
        if float(setpoint_speed) < 0 or float(setpoint_speed) > 43.496:
            alert = Alert("Invalid speed entered!")
            alert.exec_()
            return

        # Check if speed entered is less than command speed
        com_sp = self.findChild(QtWidgets.QLabel, "command_speed_label").text()
        com_sp = com_sp.split()[0]
        if float(setpoint_speed) > float(com_sp):
            alert = Alert("Error! Entered speed must be lower than speed limit!")
            alert.exec_()
            return

        # If all conditions pass, check for confirmation
        confirmation = Confirmation("Entered speed is valid!\nSet speed?")
        response = confirmation.exec_()
        if response == False:
            return
        else:
            signals.swtrain_gui_set_setpoint_speed.emit(int(self.current_train_id) - 1, float(setpoint_speed))

        # Clear setpoint speed text box
        self.EnterSpeed.clear()
        self.update_gui()

    def toggle_service_brake(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # If no kp and ki have been set, service brake cannot be removed
        kp = self.findChild(QtWidgets.QLabel, 'KpLabel').text()
        kp = kp.split()[0]
        if float(kp) == 0.0:
            alert = Alert("Error: Must set Kp and Ki in order to remove service brake!")
            alert.exec_()
            return

        # Check if authority is zero NEED METHOD TO AUTOMATICALLY TURN SERVICE BRAKE ON AUTOMATICALLY
        #if control_system.p_controllers[int(self.current_train_id) - 1].authority == 0:
            #self.service_brake.setStyleSheet("background-color: rgb(255, 51, 16);")
            # Send signal to notify status of service brake
            #signals.swtrain_gui_press_service_brake.emit(int(self.current_train_id) - 1)

        if self.service_brake.styleSheet() == "background-color: green;":
                #Confirm use of service brake
                confirmation = Confirmation("Turn service brake on?")
                response = confirmation.exec_()
                if response == True:
                    self.service_brake.setStyleSheet("background-color: rgb(255, 51, 16);")
                    # Send signal to notify status of service brake
                    signals.swtrain_gui_press_service_brake.emit(int(self.current_train_id) - 1)
                else:
                    return
        else:
            #Confirm turning off service brake
            confirmation = Confirmation("Turn service brake off?")
            response = confirmation.exec_()
            if response == True:
                self.service_brake.setStyleSheet("background-color: green;")
                # Send signal to notify status of service brake
                signals.swtrain_gui_press_service_brake.emit(int(self.current_train_id) - 1)
            else:
                return
            
        #alert = Alert("Service brake cannot be activated until authority is 0!")
        #alert.exec_()
        return
    
    def toggle_emergency_brake(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return
        
        if self.emergency_brake.styleSheet() == "background-color: green;":
                #Confirm use of emergency brake
                confirmation = Confirmation("Turn emergency brake on?")
                response = confirmation.exec_()
                if response == True:
                    self.emergency_brake.setStyleSheet("background-color: rgb(255, 51, 16);")
                    # Send signal to notify status of emergency brake
                    signals.swtrain_gui_pull_ebrake.emit(int(self.current_train_id) - 1)
                else:
                    return
        else:
            #Confirm turning off emergency brake
            confirmation = Confirmation("Turn emergency brake off?")
            response = confirmation.exec_()
            if response == True:
                self.emergency_brake.setStyleSheet("background-color: green;")
                # Send signal to notify status of emergency brake
                signals.swtrain_gui_release_ebrake.emit(int(self.current_train_id) - 1)
            else:
                return


    def save_inputs(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Get Kp and Ki
        Kp = self.findChild(QtWidgets.QLineEdit, "InputKp").text()
        Ki = self.findChild(QtWidgets.QLineEdit, "InputKi").text()

        # Check to make sure values entered are integers
        try:
            int(Kp)
        except ValueError:
            alert = Alert("Kp must be an integer value")
            alert.exec_()
            return

        try:
            int(Ki)
        except ValueError:
            alert = Alert("Ki must be an integer value")
            alert.exec_()
            return

        # Make sure sure values entered are not negative
        if int(Kp) <= 0:
            alert = Alert("Invalid Kp entered!")
            alert.exec_()
            return

        if int(Ki) <= 0:
            alert = Alert("Invalid Ki entered!")
            alert.exec_()
            return

        # Ask for confirmation to ensure values are as desired
        confirmation = Confirmation("Confirm Kp and Ki:")
        response = confirmation.exec_()
        if response == False:
            return

        signals.swtrain_gui_set_kp_ki.emit(int(self.current_train_id) - 1, float(Kp), float(Ki))

        # Clear Kp and Ki text boxes
        self.InputKp.clear()
        self.InputKi.clear()

        self.update_gui()

    def use_defaults(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return

        # Ask for confirmation to ensure values are as desired
        confirmation = Confirmation("Do you want to use the default values?")
        response = confirmation.exec_()
        if response == False:
            return

        signals.swtrain_gui_set_kp_ki.emit(int(self.current_train_id) - 1, float(35000), float(1000))
        self.update_gui()

    def resolve_brake_failure(self):
        # If no controllers have been created, button does nothing
        if self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentText() == "":
            alert = Alert("Error: No trains have been dispatched!")
            alert.exec_()
            return
        
        # Check to see if there is a failure occurring
        if self.brake_failure_status.styleSheet() == "background-color: green;":
            alert = Alert("Error: No brake failure has occurred!")
            alert.exec_()
            return

        # If failure has occurred, resolve the failure
        alert = Alert("Brake failure is being resolved please wait one minute.")
        alert.exec_()
        signals.swtrain_resolve_failure.emit(int(self.current_train_id) - 1)
        self.update_gui()

    def logout(self):
        # This is executed when the button is pressed
        window_list.remove(self)
        self.close()

    # def stop_all_timers(self):
    #     self.main_menu_timer.stop()
        #self.controller_info_timer.stop()
        #self.failure_info_timer.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    windows = SWTrainUi()
    app.exec_()