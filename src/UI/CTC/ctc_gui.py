import os
from PyQt5 import QtWidgets, uic, QtCore
import sys

sys.path.insert(1, '../../src')
from server_functions import *

# GLOBALS
class Ui(QtWidgets.QMainWindow):

	# UI Class initializer
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('UI/ctc_main.ui', self)
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
		self.button.clicked.connect(self.MapWindow)

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
		uic.loadUi('UI/ctc_schedule_import.ui', self)
		self.setWindowTitle("CTC - Load Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)


	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Edit Schedule Page
	#######################################################################################################################################
	#######################################################################################################################################
	def EditScheduleWindow(self):
		uic.loadUi('UI/ctc_schedule_edit.ui', self)
		self.setWindowTitle("CTC - Edit Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'ScheduleSaveButton') # Find the button
		self.button.clicked.connect(self.saveEditedSchedule)

	def saveEditedSchedule(self):
		app.exit()



	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Dispatch Train Window
	#######################################################################################################################################
	#######################################################################################################################################
	def DispatchTrainWindow(self):

		uic.loadUi('UI/ctc_dispatch_train.ui', self)
		self.setWindowTitle("CTC - Dispatch Train")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)

		self.d_block_label = self.findChild(QtWidgets.QLineEdit, 'BlockInput') # Find the text input
		self.d_time_label = self.findChild(QtWidgets.QLineEdit, 'TimeInput') # Find the input

		self.d_conf_label = self.findChild(QtWidgets.QLabel, 'ConfirmationLabel') # Find the label

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

		# Error Check time values
		try:
			int(self.d_time_label.text()[0] + self.d_time_label.text()[1])
		except:
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		try:
			int(self.d_time_label.text()[3] + self.d_time_label.text()[4])
		except:
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return

		# Error Check for time value
		if(len(self.d_time_label.text()) != 6):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		elif(int(self.d_time_label.text()[0] + self.d_time_label.text()[1]) not in range(1, 13)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		elif(int(self.d_time_label.text()[3] + self.d_time_label.text()[4]) not in range(60)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		elif(self.d_time_label.text()[5] not in ['a', 'p']):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time of Day  Entered (a/p)')
		# Error Check for block value
		elif((int(self.d_block_label.text()) < 0) | (len(self.d_block_label.text()) == 0)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered')
			return

		# Print confirmation to screen and take actions if information valid
		else:
			self.d_conf_label.setStyleSheet("color: green")
			self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text() + ' at ' + self.d_time_label.text())

		##### Send data to server #####
		##### data = "block hour minute a/p"
		send_message(RequestCode.CTC_DISPATCH_TRAIN, self.d_block_label.text() + ' ' + self.d_time_label.text()[0] + self.d_time_label.text()[1] + ' ' + self.d_time_label.text()[3] + self.d_time_label.text()[4]+ ' ' + self.d_time_label.text()[5])

		

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Map Window
	#######################################################################################################################################
	#######################################################################################################################################
	def MapWindow(self):
		uic.loadUi('UI/ctc_view_map.ui', self)
		self.setWindowTitle("CTC - View Map")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)

	# Return to Main from all different windows
	def returnToMainWindow(self):
		uic.loadUi('UI/ctc_main.ui', self)
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
		self.button.clicked.connect(self.MapWindow)

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
		#app.exit()

	#######################################################################################################################################
	#######################################################################################################################################
	# Exits the Module
	#######################################################################################################################################
	#######################################################################################################################################
	def ExitModule(self):
		app.exit()









# Main
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()



