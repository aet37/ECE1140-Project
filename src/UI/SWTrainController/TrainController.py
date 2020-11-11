import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
sys.path.insert(1, 'src')
from UI.server_functions import *
from UI.Common.common import Alert

class SWTrainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super(SWTrainUi, self).__init__()
        uic.loadUi('src/UI/SWTrainController/TrainController.ui', self)

        # Create timer to update pages
        self.train_actions_timer = QTimer()
        #self.train_actions_timer.timeout.connect(self.update_data)

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
        ##########################################

        # Start timer to update train actions page
        self.stopAllTimers()
        self.train_actions_timer.start(250)

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

    def set_button_state(self, index):
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.return_button1.setEnabled(True)
        self.return_button2.setEnabled(True)

    def toggle_lights(self):
        # Potential line for determining train ID to send
        # self.findChild(QtWidgets.QComboBox, "TrainIDBox2").currentText()
        send_message(RequestCode.SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS, "1")

    def toggle_doors(self):
        # Potential line for determining train ID to send
        # self.findChild(QtWidgets.QComboBox, "TrainIDBox2").currentText()
        send_message(RequestCode.SWTRAIN_GUI_TOGGLE_DAMN_DOORS, "1")

    def toggle_announcements(self):
        # Potential line for determining train ID to send
        # self.findChild(QtWidgets.QComboBox, "TrainIDBox2").currentText()
        send_message(RequestCode.SWTRAIN_GUI_ANNOUNCE_STATIONS, "1")

    def toggle_ads(self):
        # Potential line for determining train ID to send
        # self.findChild(QtWidgets.QComboBox, "TrainIDBox2").currentText()
        send_message(RequestCode.SWTRAIN_GUI_DISPLAY_ADS, "1")

    def set_SeanPaul(self):
        # Potential line for determining train ID to send
        # self.findChild(QtWidgets.QComboBox, "TrainIDBox2").currentText()
        temp = self.findChild(QtWidgets.QLineEdit, "InputTemp").text()
        try:
            int(temp)
        except ValueError:
            alert = Alert("Temperature must be an integer value")
            alert.exec_()
            return

        if int(temp) < 64 or int(temp) > 80 :
            alert = Alert("Invalid Temperature!")
            alert.exec_()
            return
        
        # If input temperature is valid, send request code
        send_message(RequestCode.SWTRAIN_GUI_SET_SEAN_PAUL, ("1" + " " + temp) )

    def toggle_mode1(self):
        # Toggle color of mode boxes
        self.automatic_mode.setStyleSheet("background-color: green;")
        self.manual_mode.setStyleSheet("background-color: rgb(255, 51, 16);")
            
        #send_message(RequestCode.SWTRAIN_GUI_SWITCH_MODE, "1")

    def toggle_mode2(self):
        # Toggle color of mode boxes
        self.automatic_mode.setStyleSheet("background-color: rgb(255, 51, 16);")
        self.manual_mode.setStyleSheet("background-color: green;")
            
        #send_message(RequestCode.SWTRAIN_GUI_SWITCH_MODE, "1")

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

    def stopAllTimers(self):
        self.train_actions_timer.stop()

app = QtWidgets.QApplication(sys.argv)
windows = SWTrainUi()
app.exec_()