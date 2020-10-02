import os
from PyQt5 import QtWidgets, uic
import sys

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


	############################
	# Opens Load Schedule Page
	############################
	def LoadScheduleWindow(self):
		uic.loadUi('UI/ctc_schedule_import.ui', self)
		self.setWindowTitle("CTC - Load Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)


	############################
	# Opens Edit Schedule Page
	############################
	def EditScheduleWindow(self):
		uic.loadUi('UI/ctc_schedule_edit.ui', self)
		self.setWindowTitle("CTC - Edit Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'ScheduleSaveButton') # Find the button
		self.button.clicked.connect(self.saveEditedSchedule)

	def saveEditedSchedule(self):
		app.exit()



	###############################
	# Opens Dispatch Train Window
	###############################
	def DispatchTrainWindow(self):

		uic.loadUi('UI/ctc_dispatch_train.ui', self)
		self.setWindowTitle("CTC - Dispatch Train")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)

		self.blue_radio_button = self.findChild(QtWidgets.QRadioButton, 'BlueLineRadio') # Find the radio button
		self.green_radio_button = self.findChild(QtWidgets.QRadioButton, 'GreenLineRadio') # Find the radio button

		self.d_block_label = self.findChild(QtWidgets.QLineEdit, 'BlockInput') # Find the label
		self.d_time_label = self.findChild(QtWidgets.QLineEdit, 'TimeInput') # Find the label

		self.button = self.findChild(QtWidgets.QPushButton, 'DispatchButton') # Find the button
		self.button.clicked.connect(self.DispatchTrain)


	def DispatchTrain(self):
		print(self.d_block_label.text(), '   ', self.d_time_label.text())

		if(self.blue_radio_button.isChecked()):
			print('BLUE')
		if(self.green_radio_button.isChecked()):
			print('GREEN')

	############################
	# Opens Map Window
	############################
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


	#############################
	# Toggle for Automatic Mode
	#############################
	def ToggleAutomaicMode(self):
		return None
		#app.exit()

	############################
	# Exits the Module
	############################
	def ExitModule(self):
		app.exit()









# Main
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()



