import os
from PyQt5 import QtWidgets, uic, QtCore
import sys

sys.path.insert(1, 'src/UI')
from server_functions import *

# GLOBALS
class CTCUi(QtWidgets.QMainWindow):

	# UI Class initializer
	def __init__(self):
		super(CTCUi, self).__init__()
		uic.loadUi('src/UI/CTC/ctc_main.ui', self)

		self.setWindowTitle("CTC Main Page")

		# In Main Window
		self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
		self.button.clicked.connect(self.LoadScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'EditSchedule') # Find the button
		self.button.clicked.connect(self.EditScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
		self.button.clicked.connect(self.ExitModule)
		self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
		self.button.clicked.connect(self.DispatchTrainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
		self.button.clicked.connect(self.MapMenuWindow)

		self.checkbox = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
		self.checkbox.clicked.connect(self.ToggleAutomaicMode)

		self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label

		self.show()


	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Load Schedule Page
	#######################################################################################################################################
	#######################################################################################################################################
	def LoadScheduleWindow(self):
		uic.loadUi('src/UI/CTC/ctc_schedule_import.ui', self)
		self.setWindowTitle("CTC - Load Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)


	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Edit Schedule Page
	#######################################################################################################################################
	#######################################################################################################################################
	def EditScheduleWindow(self):
		uic.loadUi('src/UI/CTC/ctc_schedule_edit.ui', self)
		self.setWindowTitle("CTC - Edit Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'ScheduleSaveButton') # Find the button
		self.button.clicked.connect(self.saveEditedSchedule)

	def saveEditedSchedule(self):
		app.exit()

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Map Menu Page
	#######################################################################################################################################
	#######################################################################################################################################
	def MapMenuWindow(self):
		uic.loadUi('src/UI/CTC/ctc_map_menu.ui', self)
		self.setWindowTitle("CTC - Map Menu")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button to return to main menu
		self.button.clicked.connect(self.returnToMainWindow)

		self.button = self.findChild(QtWidgets.QPushButton, 'ViewGreen') # Find the view green button
		self.button.clicked.connect(self.GreenMapWindow)

		self.button = self.findChild(QtWidgets.QPushButton, 'ViewRed') # Find the view green button
		self.button.clicked.connect(self.RedMapWindow)

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Dispatch Train Window
	#######################################################################################################################################
	#######################################################################################################################################
	def DispatchTrainWindow(self):
		uic.loadUi('src/UI/CTC/ctc_dispatch_train.ui', self)
		self.setWindowTitle("CTC - Dispatch Train")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)

		self.green_radio = self.findChild(QtWidgets.QRadioButton, 'GreenRadio')
		self.red_radio = self.findChild(QtWidgets.QRadioButton, 'RedRadio')

		self.d_block_label = self.findChild(QtWidgets.QLineEdit, 'BlockInput') # Find the text input
		self.d_time_label = self.findChild(QtWidgets.QLineEdit, 'TimeInput') # Find the input

		self.d_conf_label = self.findChild(QtWidgets.QLabel, 'ConfirmationLabel') # Find the label
		self.d_speed_label = self.findChild(QtWidgets.QLabel, 'SpeedOut') # Find the label
		self.d_auth_label = self.findChild(QtWidgets.QLabel, 'AuthorityOut') # Find the label

		self.button = self.findChild(QtWidgets.QPushButton, 'DispatchButton') # Find the button
		self.button.clicked.connect(self.DispatchTrain)


	def DispatchTrain(self):
		# Error Check block value
		try:
			int(self.d_block_label.text())
		except:
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered')
			return

		# Make sure user specified a line
		if((self.green_radio.isChecked() == False) & (self.red_radio.isChecked() == False)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Please Select a Line')
			return

		# Error Check for block value
		if((int(self.d_block_label.text()) <= 0) | (len(self.d_block_label.text()) == 0)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered')
			return
		elif((self.red_radio.isChecked()) & (int(self.d_block_label.text()) > 76)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered For Red Line')
			return
		elif((self.red_radio.isChecked() == False) & (int(self.d_block_label.text()) > 155)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered For Green Line')
			return

		# Error Check for time value
		if((len(self.d_time_label.text()) != 6) & (len(self.d_time_label.text()) != 0)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered 3')
			return
		elif(len(self.d_time_label.text()) == 6):

			# Error Check time values
			try:
				int(self.d_time_label.text()[0] + self.d_time_label.text()[1])
			except:
				self.d_conf_label.setStyleSheet("color: red")
				self.d_conf_label.setText('Error: Invalid Time Entered 1')
				return
			try:
				int(self.d_time_label.text()[3] + self.d_time_label.text()[4])
			except:
				self.d_conf_label.setStyleSheet("color: red")
				self.d_conf_label.setText('Error: Invalid Time Entered 2')
				return

			if(int(self.d_time_label.text()[0] + self.d_time_label.text()[1]) not in range(1, 13)):
				self.d_conf_label.setStyleSheet("color: red")
				self.d_conf_label.setText('Error: Invalid Time Entered 4')
				return
			elif(int(self.d_time_label.text()[3] + self.d_time_label.text()[4]) not in range(60)):
				self.d_conf_label.setStyleSheet("color: red")
				self.d_conf_label.setText('Error: Invalid Time Entered 5')
				return
			elif(self.d_time_label.text()[5] not in ['a', 'p']):
				self.d_conf_label.setStyleSheet("color: red")
				self.d_conf_label.setText('Error: Invalid Time of Day  Entered (a/p)')

			# Print confirmation to screen and take actions if information valid
			else:
				self.d_conf_label.setStyleSheet("color: green")
				self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text() + ' at ' + self.d_time_label.text())
				self.d_speed_label.setText('Command Speed [to Track Controller]: 55 km/hr')
				self.d_auth_label.setText('Authority [to Track Controller]: 3 Blocks')
				##### Send data to server #####
				##### data = "block hour minute a/p"
				send_message(RequestCode.CTC_DISPATCH_TRAIN,  str(int(self.red_radio.isChecked())) + ' ' + self.d_time_label.text()[0] + self.d_time_label.text()[1] + ' ' + self.d_time_label.text()[3] + self.d_time_label.text()[4]+ ' ' + self.d_time_label.text()[5] + ' ' + self.d_block_label.text())

		else:
			self.d_conf_label.setStyleSheet("color: green")
			self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text() + ' Now')
			self.d_speed_label.setText('Command Speed [to Track Controller]: 55 km/hr')
			self.d_auth_label.setText('Authority [to Track Controller]: 3 Blocks')
			send_message(RequestCode.CTC_DISPATCH_TRAIN,  str(int(self.red_radio.isChecked())) + ' 00 00 a ' + self.d_block_label.text())


		##### Send data to server #####
		##### data = "block hour minute a/p"
		#send_message(RequestCode.CTC_DISPATCH_TRAIN,  '0' + ' ' + self.d_time_label.text()[0] + self.d_time_label.text()[1] + ' ' + self.d_time_label.text()[3] + self.d_time_label.text()[4]+ ' ' + self.d_time_label.text()[5] + ' ' + self.d_block_label.text())

		

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Green Map Window
	#######################################################################################################################################
	#######################################################################################################################################
	def GreenMapWindow(self):
		global time_timr
		uic.loadUi('src/UI/CTC/ctc_view_green_line.ui', self)
		self.setWindowTitle("CTC - View Green Map")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMapMenu') # Find the button
		self.button.clicked.connect(self.LeaveThis)

		self.SigButton = self.findChild(QtWidgets.QPushButton, 'ViewSignalButton')	# Find signal button
		self.SigButton.clicked.connect(self.ViewSignalGreenGo)

		# Automatically refresh Map after 700ms

		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.RefreshMapGreen)
		time_timr.start(700)

		# Find the Blocks
		for i in range(1, 151):
			exec('self.GB%s = self.findChild(QtWidgets.QPushButton, \'G%s\')' % (str(i), str(i)))

		 # Find the Switches
		for i in range(1, 7):
			exec('self.S%s = self.findChild(QtWidgets.QPushButton, \'SW%s\')' % (str(i), str(i)))

	def RefreshMapGreen(self):
		# Ping server for track occupancies
		m_tuple_data = send_message(RequestCode.CTC_SEND_GUI_GREEN_OCCUPANCIES)

		# Extract string data from tuple
		m_data = m_tuple_data[1]

		for i in range(len(m_data)):
			if(m_data[i] == 't'):
				try:
					eval('self.GB%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")' % str(i + 1))		# if occupied change block color to yellow
				except:
					print(i, 'Warning: Screen has been closed before button could update')
			else:
				try:
					eval('self.GB%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")' % str(i + 1))		# if not occupied, change block color to green
				except:
					print('Warning: Screen has been closed before  button could update')

		# Ping server for track occupancies
		m_tuple_data = send_message(RequestCode.CTC_SEND_GUI_SWITCH_POS_GREEN)

		# Extract string data from tuple
		m_data = m_tuple_data[1]

		for i in range(1, 7):
			wrtxt = m_data[(4 * (i - 1)):(3 + (4 * (i - 1)))]
			try:
				eval('self.SW%s.setText(\'%s\')' % (str(i), wrtxt))
			except:
				print('Warning: Screen has been closed before button could update')

	def ViewSignalGreenGo(self):
		global time_timr
		time_timr.stop()
		self.ViewSignalGreen()

	def LeaveThis(self):
		global time_timr
		time_timr.stop()
		self.MapMenuWindow()

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Green Signal Info Window
	#######################################################################################################################################
	#######################################################################################################################################
	def ViewSignalGreen(self):
		uic.loadUi('src/UI/CTC/ctc_view_signal_green_line.ui', self)
		self.setWindowTitle("CTC - View Green Line Signal")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.GreenMapWindow)

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Red Map Window
	#######################################################################################################################################
	#######################################################################################################################################
	def RedMapWindow(self):
		global time_timr
		uic.loadUi('src/UI/CTC/ctc_view_red_line.ui', self)
		self.setWindowTitle("CTC - View Red Map")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMapMenu') # Find the button
		self.button.clicked.connect(self.LeaveThis)

		self.SigButton = self.findChild(QtWidgets.QPushButton, 'ViewSignalButton')	# Find signal button
		self.SigButton.clicked.connect(self.ViewSignalRedGo)

		# Automatically refresh Map after 700ms

		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.RefreshMapRed)
		time_timr.start(700)

		# Find the Blocks
		for i in range(1, 77):
			exec('self.R%s = self.findChild(QtWidgets.QPushButton, \'RB%s\')' % (str(i), str(i)))

		 # Find the Switches
		for i in range(1, 8):
			exec('self.S%s = self.findChild(QtWidgets.QPushButton, \'SW%s\')' % (str(i), str(i)))

	def RefreshMapRed(self):
		# Ping server for track occupancies
		m_tuple_data = send_message(RequestCode.CTC_SEND_GUI_RED_OCCUPANICES)

		# Extract string data from tuple
		m_data = m_tuple_data[1]

		for i in range(len(m_data)):
			if(m_data[i] == 't'):
				try:
					eval('self.R%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")' % str(i + 1))		# if occupied change block color to yellow
				except:
					print(i, 'Warning: Screen has been closed before button could update')
			else:
				try:
					eval('self.R%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")' % str(i + 1))		# if not occupied, change block color to green
				except:
					print('Warning: Screen has been closed before  button could update')

		# Ping server for switch positions
		m_tuple_data = send_message(RequestCode.CTC_SEND_GUI_SWITCH_POS_RED)

		# Extract string data from tuple
		m_data = m_tuple_data[1]

		for i in range(1, 8):
			wrtxt = m_data[(4 * (i - 1)):(3 + (4 * (i - 1)))]
			try:
				eval('self.SW%s.setText(\'%s\')' % (str(i), wrtxt))
			except:
				print('Warning: Screen has been closed before button could update')

	def ViewSignalRedGo(self):
		global time_timr
		time_timr.stop()
		self.ViewSignalRed()

	def LeaveThis(self):
		global time_timr
		time_timr.stop()
		self.MapMenuWindow()

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Red Signal Info Window
	#######################################################################################################################################
	#######################################################################################################################################
	def ViewSignalRed(self):
		uic.loadUi('src/UI/CTC/ctc_view_signal_red_line.ui', self)
		self.setWindowTitle("CTC - View Green Line Signal")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.RedMapWindow)

	#######################################################################################################################################
	#######################################################################################################################################
	# Return to main window from all windows function
	#######################################################################################################################################
	#######################################################################################################################################
	def returnToMainWindow(self):
		uic.loadUi('src/UI/CTC/ctc_main.ui', self)
		self.setWindowTitle("CTC Main Page")

		# In Main Window
		self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
		self.button.clicked.connect(self.LoadScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'EditSchedule') # Find the button
		self.button.clicked.connect(self.EditScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
		self.button.clicked.connect(self.ExitModule)
		self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
		self.button.clicked.connect(self.DispatchTrainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
		self.button.clicked.connect(self.MapMenuWindow)

		self.checkbox = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
		self.checkbox.clicked.connect(self.ToggleAutomaicMode)

		self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label


	#######################################################################################################################################
	#######################################################################################################################################
	# Toggle for Automatic Mode
	#######################################################################################################################################
	#######################################################################################################################################
	def ToggleAutomaicMode(self):
		return None

	#######################################################################################################################################
	#######################################################################################################################################
	# Exits the Module
	#######################################################################################################################################
	#######################################################################################################################################
	def ExitModule(self):
		if(sys.platform == 'darwin'):
			os.system('python3 src/UI/login_gui.py &')
		else:
			os.system('start /B python src/UI/login_gui.py')
		app.exit()


app = QtWidgets.QApplication(sys.argv)
window = CTCUi()
app.exec_()



