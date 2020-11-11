import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
sys.path.insert(1, 'src')
from UI.server_functions import *
from UI.Common.common import Alert, Confirmation

class SWTrainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super(SWTrainUi, self).__init__()

        # Define timers
        self.main_menu_timer = QTimer()
        #self.controller_info_timer = QTimer()
        #self.failure_info_timer = QTimer()
        self.main_menu_timer.timeout.connect(self.update_controller_list)
        #self.controller_info_timer.timeout.connect(self.update_gui1)
        #self.failure_info_timer.timeout.connect(self.update_gui2)

        # Define current train id
        self.current_train_id = "1"

        uic.loadUi('src/UI/SWTrainController/TrainController.ui', self)
        self.stop_all_timers() # Restart timers
        self.main_menu_timer.start(2000) # 2 seconds
        
        self.TrainIDBox.currentIndexChanged.connect(self.update_current_train_id) # Dropdown box
        self.TrainIDBox2.currentIndexChanged.connect(self.update_current_train_id2) # Dropdown box
        self.TrainIDBox3.currentIndexChanged.connect(self.update_current_train_id3) # Dropdown box

        # Initialize all buttons and the page of the UI
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.stacked_widget.setCurrentIndex(0)

        # Define which pages buttons will take you to
        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Define which functions are called when MainWindow buttons are selected
        # When doors button is clicked, go to toggle_doors function
        self.doors_button.clicked.connect(self.toggle_doors)

        # When light button is clicked, go to toggle_lights function
        self.lights_button.clicked.connect(self.toggle_lights)

        # When announcements button is clicked, go to toggle_announcements function
        self.announceStations_button.clicked.connect(self.toggle_announcements)

        # When advertisements button is clicked go to toggle_ads function
        self.ads_button.clicked.connect(self.toggle_ads)

        # When temperature button is clicked go to set_SeanPaul function
        self.sean_paul_buttton.clicked.connect(self.set_SeanPaul)

        # When User wants to toggle mode, go to toggle_mode function
        self.automatic_mode.clicked.connect(self.toggle_mode1)
        self.manual_mode.clicked.connect(self.toggle_mode2)

        # When set setpoint button is clicked, go to set_setpoint function
        self.set_setpoint_speed.clicked.connect(self.set_setpoint)

        # When service brake button is clicked, go to toggle_service_brake function
        self.service_brake.clicked.connect(self.toggle_service_brake)
        ##########################################

        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.return_button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.return_button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Define logout button
        self.logout_button = self.findChild(QtWidgets.QPushButton, 'Logout') # Find the button
        self.logout_button.clicked.connect(self.logout)
        self.logout_button2 = self.findChild(QtWidgets.QPushButton, 'Logout2') # Find the button
        self.logout_button2.clicked.connect(self.logout)
        self.logout_button3 = self.findChild(QtWidgets.QPushButton, 'Logout3') # Find the button
        self.logout_button3.clicked.connect(self.logout)

        self.show()
    
    # Initialize buttons in UI
    def initUI(self):
        # Define buttons on main page
        self.button1 = self.findChild(QtWidgets.QPushButton, 'TrainActions') # Find the button
        self.button2 = self.findChild(QtWidgets.QPushButton, 'Information') # Find the button
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget') # Find stacked widget

        # Define buttons on Train Actions Page
        self.return_button1 = self.findChild(QtWidgets.QPushButton, 'MainMenu2')
        
        # Define button for doors
        self.doors_button = self.findChild(QtWidgets.QPushButton, 'Doors')
        
        # Define button for lights
        self.lights_button = self.findChild(QtWidgets.QPushButton, 'Lights')
        
        # Define button for announcements
        self.announceStations_button = self.findChild(QtWidgets.QPushButton, 'Announcements')
        
        # Define button for advertisements
        self.ads_button = self.findChild(QtWidgets.QPushButton, 'Advertisements')
        
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

        self.defineToggles()

        #Define buttons on Information Page
        self.return_button2 = self.findChild(QtWidgets.QPushButton, 'MainMenu3')

    def defineToggles(self):
        # Give buttons capability to toggle in appearance
        self.doors_button.setCheckable(True)
        self.doors_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.lights_button.setCheckable(True)
        self.lights_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.announceStations_button.setCheckable(True)
        self.announceStations_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")
        self.ads_button.setCheckable(True)
        self.ads_button.setStyleSheet("QPushButton{background-color:green;}QPushButton:checked{background-color:rgb(255, 51, 16);}")

    def update_current_train_id(self):
        self.current_train_id = self.TrainIDBox.currentText()
    
    def update_current_train_id2(self):
        self.current_train_id = self.TrainIDBox2.currentText()
    
    def update_current_train_id3(self):
        self.current_train_id = self.TrainIDBox3.currentText()

    def update_controller_list(self):
        # Update the drop down
        responsecode, dataReceived = send_message(RequestCode.SWTRAIN_GUI_UPDATE_DROP_DOWN)
        if responsecode == ResponseCode.SUCCESS:
            # Parse the data and update the gui.
            dataParsed = int(dataReceived)
            count = 1
            currentIndex = self.findChild(QtWidgets.QComboBox, 'TrainIDBox').currentIndex()
            currentIndex2 = self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').currentIndex()
            currentIndex3 = self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').currentIndex()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox').clear()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').clear()
            self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').clear()
            while(count < dataParsed + 1):
                self.TrainIDBox.addItem(str(count))
                self.TrainIDBox2.addItem(str(count))
                self.TrainIDBox3.addItem(str(count))
                count = count + 1

            # Update all dropdowns depending on which page is up
            if self.stacked_widget.currentIndex() == 0:
                self.update_current_train_id()
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex)
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex)
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex)
            elif self.stacked_widget.currentIndex() == 1:
                self.update_current_train_id2()
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex2)
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex2)
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex2)
            else:
                self.update_current_train_id3()
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox').setCurrentIndex(currentIndex3)
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox2').setCurrentIndex(currentIndex3)
                self.findChild(QtWidgets.QComboBox, 'TrainIDBox3').setCurrentIndex(currentIndex3)

        if "" in self.current_train_id:
            return

        # Update Train's info
        responsecode, dataReceived = send_message(RequestCode.SWTRAIN_GUI_GATHER_DATA, str(self.current_train_id))
        if responsecode == ResponseCode.SUCCESS:
            # Parse the data and update the gui.
            dataParsed = dataReceived.split()

            # Store all data into individual variables
            self.doors_status = dataParsed[0]
            self.lights_status = dataParsed[1]
            self.announcements_status = dataParsed[2]
            self.advertisements_status = dataParsed[3]
            self.curr_speed = dataParsed[4]
            self.com_speed = dataParsed[5]
            self.setpoint_speed = dataParsed[6]
            self.service_brake_status = dataParsed[7]
            self.current_mode = dataParsed[8]

            # Change GUI to reflect current data
            if self.doors_status == "1":
                self.doors_button.setStyleSheet("background-color: rgb(255, 51, 16);")
            else:
                self.doors_button.setStyleSheet("background-color: green;")
            

            #self.findChild(QtWidgets.QLabel, 'disp_acceleration_limit').setText(dataParsed[0] + " m/s²")
            #self.findChild(QtWidgets.QLabel, 'disp_deceleration_limit').setText(dataParsed[1] + " m/s²")
            #self.findChild(QtWidgets.QLabel, 'disp_block_elevation').setText(dataParsed[2] + " m")
            #self.findChild(QtWidgets.QLabel, 'disp_block_slope').setText(dataParsed[3] + " m/s")
            # UPDATE POSITION HERE
            #self.findChild(QtWidgets.QLabel, 'disp_block_size').setText(dataParsed[4] + " m")
            #self.findChild(QtWidgets.QLabel, 'disp_current_block').setText("block #" + dataParsed[5])
            #self.findChild(QtWidgets.QLabel, 'disp_destination_block').setText("block #" + dataParsed[6])
    
    def set_button_state(self, index):
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.return_button1.setEnabled(True)
        self.return_button2.setEnabled(True)

    def toggle_lights(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return

        send_message(RequestCode.SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS, self.current_train_id)

    def toggle_doors(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return

        send_message(RequestCode.SWTRAIN_GUI_TOGGLE_DAMN_DOORS, self.current_train_id)

    def toggle_announcements(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return
        send_message(RequestCode.SWTRAIN_GUI_ANNOUNCE_STATIONS, self.current_train_id)

    def toggle_ads(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return
        send_message(RequestCode.SWTRAIN_GUI_DISPLAY_ADS, self.current_train_id)

    def set_SeanPaul(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return

        temp = self.findChild(QtWidgets.QLineEdit, "InputTemp").text()
        try:
            int(temp)
        except ValueError:
            alert = Alert("Temperature must be an integer value")
            alert.exec_()
            return

        if int(temp) < 64 or int(temp) > 80 :
            alert = Alert("Invalid temperature!")
            alert.exec_()
            return
        
        # If input temperature is valid, send request code
        send_message(RequestCode.SWTRAIN_GUI_SET_SEAN_PAUL, (self.current_train_id + " " + temp) )

    def toggle_mode1(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
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
            
        send_message(RequestCode.SWTRAIN_GUI_SWITCH_MODE, "1")

    def toggle_mode2(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
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
   
        send_message(RequestCode.SWTRAIN_GUI_SWITCH_MODE, "1")
    
    def set_setpoint(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return

        # Get setpoint speed
        setpoint_speed = self.findChild(QtWidgets.QLineEdit, "EnterSpeed").text()

        # Check if train is in manual mode
        if self.manual_mode.styleSheet() != "background-color: green;":
            alert = Alert("Cannot input value!\nTrain must be in manual mode!")
            alert.exec_()
            return
        
        # Check if number was entered
        try:
            int(setpoint_speed)
        except ValueError:
            alert = Alert("Setpoint speed must be an integer value")
            alert.exec_()
            return

        # Check if speed entered is within valid range
        if int(setpoint_speed) < 0 or int(setpoint_speed) > 43.496:
            alert = Alert("Invalid speed entered!")
            alert.exec_()
            return
        
        # Check if speed entered is less than command speed
        #com_sp = self.findChild(QtWidgets.QLabel, "CommandSpeedLabel").text()
        #if int(setpoint_speed) > int(com_sp):
        #    alert = Alert("Error! Entered speed must be lower than speed limit!")
        #    alert.exec_()
        #    return
        
        # If all conditions pass, check for confirmation
        confirmation = Confirmation("Entered speed is valid!\nSet speed?")
        response = confirmation.exec_()
        if response == False:
            return
        else:
            send_message(RequestCode.SWTRAIN_GUI_SET_SETPOINT_SPEED, "1")

    def toggle_service_brake(self):
        # If no controllers have been created, button does nothing
        if "" in self.current_train_id:
            return

        # Check if authority is zero
        # <check here>

        #Confirm use of service brake
        confirmation = Confirmation("Turn service brake on?")
        response = confirmation.exec_()
        if response == False:
            return
        else:
            if self.service_brake.styleSheet() == "background-color: green;":
                self.service_brake.setStyleSheet("background-color: rgb(255, 51, 16);")
            else:
                self.service_brake.setStyleSheet("background-color: green;")

            send_message(RequestCode.SWTRAIN_GUI_PRESS_SERVICE_BRAKE, "1")

    def logout(self):
        # This is executed when the button is pressed
        if(sys.platform == 'darwin'):
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

    # Define function to update displayed data
    #def update_data(self):
    #    responseCode, data = send_message(RequestCode.GET_COMMAND_SPEED)
    #    train_id, authority, command_speed, current_speed, speed_limit = data.split(" ")
    #    if responseCode == ResponseCode.SUCCESS:
    #        self.TrainIDLabel.setText(train_id)
    #        self.TrainIDLabel2.setText(train_id)
    #        self.TrainIDLabel3.setText(train_id)
    #        self.AuthorityLabel.setText(authority + " Blocks")
    #        self.CommandSpeedLabel.setText(command_speed + " MPH")
    #        self.CurrentSpeedLabel.setText(current_speed + " MPH")
    #        self.SpeedLimitLabel.setText(speed_limit + " MPH")
    #        send_message(RequestCode.SEND_TRAIN_MODEL_INFO, command_speed)

    def stop_all_timers(self):
        self.main_menu_timer.stop()
        #self.controller_info_timer.stop()
        #self.failure_info_timer.stop()

app = QtWidgets.QApplication(sys.argv)
windows = SWTrainUi()
app.exec_()