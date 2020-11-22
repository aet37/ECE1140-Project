import os
from PyQt5 import QtWidgets, uic, QtCore
import sys
from functools import partial
import pandas as pd

from src.CTC.TrainSystem import *
from src.UI.window_manager import window_list
from src.timekeeper import timekeeper

# GLOBALS
class CTCUi(QtWidgets.QMainWindow):

	# UI Class initializer
	def __init__(self):
		super(CTCUi, self).__init__()
		uic.loadUi('src/UI/CTC/ctc_main.ui', self)

		self.setWindowTitle("CTC Main Page")

		#init
		self.tnum = -1
		self.auto_mode = False
		self.num_blocks_closed_green = 0
		self.num_blocks_closed_red = 0
		self.open_file = ''

		# For reloading throughput value
		global time_timr

		# In Main Window
		self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
		self.button.clicked.connect(self.LoadScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
		self.button.clicked.connect(self.ExitModule)
		self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
		self.button.clicked.connect(self.CheckAutoMode)
		self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
		self.button.clicked.connect(self.MapMenuWindow)

		self.auto = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
		self.auto.clicked.connect(self.ToggleAutomaicMode)

		self.mode_text = self.findChild(QtWidgets.QLabel, 'automodetext')

		if self.auto_mode:
			self.auto.setChecked(True)

		self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label
		self.ShowThroughput()

		# Automatically refresh Map after 10s
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.ShowThroughput)
		time_timr.start(10000)


		self.show()

	def ShowThroughput(self):
		try:
			self.tplabel.setText(str(ctc.throughput))
		except:
			pass

	def CheckAutoMode(self):
		if self.auto_mode == True:
			self.mode_text.setText('ERROR: Cannot Dispatch in Automatic Mode')
		else:
			self.DispatchTrainWindow()

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
	
		self.chose_file = self.findChild(QtWidgets.QPushButton, 'ChoseFile') # Find the button
		self.chose_file.clicked.connect(self.ChoseAFile)

		self.upload_and_run = self.findChild(QtWidgets.QPushButton, 'UploadAndRun') # Find the button
		self.upload_and_run.clicked.connect(self.RunSchedule)

		self.file_path = self.findChild(QtWidgets.QLabel, 'FilePath') # Find the Label
		self.error_conf = self.findChild(QtWidgets.QLabel, 'ConfErr') # Find the Label

		# Initialize to blank
		self.open_file = ''

	def ChoseAFile(self):
		"""  """
		dialog = QtWidgets.QFileDialog(self)
		fname = dialog.getOpenFileName(self)

		if fname[0][-5:len(fname[0])] != '.xlsx':
			self.error_conf.setStyleSheet('color: rgb(252, 1, 7);')
			self.error_conf.setText('Please Chose an Excel File!')
		else:
			self.open_file = fname[0]
			self.file_path.setText(self.open_file)
			self.error_conf.setText('')

	def RunSchedule(self):
		"""  """
		# Trains to append to time keeper class if import sucessful
		to_add = []

		# Read the Excel File
		try:
			myxl = pd.read_excel(self.open_file, dtype=str)
		except:
			self.error_conf.setStyleSheet('color: rgb(252, 1, 7);')
			self.error_conf.setText('Could not open excel file...')
			return

		# Determine Line
		if myxl[myxl.columns[0]][0] == 'Green':
			line = Line.LINE_GREEN
		else:
			line = Line.LINE_RED

		for i in range(4, len(myxl.columns)):
			try:
				hour = int(myxl[myxl.columns[i]][0][0:2])
				muinute = int(myxl[myxl.columns[i]][0][3:5])
				temp_time_train = InterruptTrain(-1, line, hour, muinute)
				to_add.append(temp_time_train)
			except:
				self.error_conf.setStyleSheet('color: rgb(252, 1, 7);')
				self.error_conf.setText('Faulty Excel File. Please Scrupulously look for error in file.')
				return
			

		# If passed, add the trains to the time class
		for i in range(len(to_add)):
			timekeeper.ctc_trains_backlog.append(to_add[i])

		# Display Sucess on Screen
		self.file_path.setText('')
		self.open_file = ''
		self.error_conf.setStyleSheet('color: rgb(33, 255, 6);')
		self.error_conf.setText('Sucess! Schedule starting to run...')



	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Map Menu Page
	#######################################################################################################################################
	#######################################################################################################################################
	def MapMenuWindow(self):
		global time_timr

		uic.loadUi('src/UI/CTC/ctc_map_menu.ui', self)
		self.setWindowTitle("CTC - Map Menu")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button to return to main menu
		self.button.clicked.connect(self.LeaveThis)

		self.trains_label = self.findChild(QtWidgets.QLabel, 'TrainsLabel')	# Find label which displays valid trains

		self.button = self.findChild(QtWidgets.QPushButton, 'ViewGreen') # Find the view green button
		self.button.clicked.connect(self.GreenMapWindow)

		self.button = self.findChild(QtWidgets.QPushButton, 'ViewRed') # Find the view green button
		self.button.clicked.connect(self.RedMapWindow)

		self.train_id_label = self.findChild(QtWidgets.QLineEdit, 'ViewTrainNum')	# Input for Train ID
		self.error_label = self.findChild(QtWidgets.QLabel, 'ErrLabel')	# Input for Train ID
		self.train_button = self.findChild(QtWidgets.QPushButton, 'ViewTrainButton')	# Get status of train
		self.train_button.clicked.connect(self.OpenIfGood)

		self.UpdateTrainsList()

		# Automatically refresh Map after 1s
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.UpdateTrainsList)
		time_timr.start(1000)


	def UpdateTrainsList(self):
		if len(ctc.train_numbers) == 0:
			try:
				self.trains_label.setText('NO TRAINS DISPATCHED')
			except:
				pass
		else:
			try:
				self.trains_label.setText(str(ctc.train_numbers))
			except:
				pass



	def OpenIfGood(self):
		if(self.train_id_label.text() == ''):
			return
		else:
			try:
				int(self.train_id_label.text())
			except:
				self.error_label.setStyleSheet("color: red")
				self.error_label.setText('Error: Invalid Train Num Entered')
				return

			if(int(self.train_id_label.text()) < 1):
				self.error_label.setStyleSheet("color: red")
				self.error_label.setText('Error: Invalid Train Num Entered')
				return

			valid = int(self.train_id_label.text()) in ctc.train_numbers

			if(valid == True):	# If sucessfuly found the train in the system
				self.tnum = int(self.train_id_label.text())
				self.TrainInfoWindow()
			else:
				self.error_label.setStyleSheet("color: red")
				self.error_label.setText('Error: Invalid Train Num Entered')

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

				##### Send to Timekeeper class #####
				hr = int(self.d_time_label.text()[0:2])
				if hr == 12:
					if self.d_time_label.text()[5] == 'a':
						hr = 0
				elif self.d_time_label.text()[5] == 'p':
					hr += 12
				else:
					pass
				minute = int(self.d_time_label.text()[3:5])

				if self.red_radio.isChecked():
					temp_time_train = InterruptTrain(int(self.d_block_label.text()), Line.LINE_RED, hr, minute)
				else:
					temp_time_train = InterruptTrain(int(self.d_block_label.text()), Line.LINE_GREEN, hr, minute)

				# Add the train to the interrupt list
				timekeeper.ctc_trains_backlog.append(temp_time_train)
		else:
			self.d_conf_label.setStyleSheet("color: green")
			self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text() + ' Now')
			self.d_speed_label.setText('Command Speed [to Track Controller]: 55 km/hr')
			self.d_auth_label.setText('Authority [to Track Controller]: 3 Blocks')
			if self.red_radio.isChecked():
				ctc.DispatchTrain(int(self.d_block_label.text()), Line.LINE_RED)
			else:
				ctc.DispatchTrain(int(self.d_block_label.text()), Line.LINE_GREEN)
		
	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Train Information Window
	#######################################################################################################################################
	#######################################################################################################################################
	def TrainInfoWindow(self):
		global time_timr
		uic.loadUi('src/UI/CTC/ctc_view_train.ui', self)
		self.setWindowTitle("CTC - View Train Info")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMapMenu') # Find the button
		self.button.clicked.connect(self.LeaveThis)

		self.location = self.findChild(QtWidgets.QLabel, 'BlockLabel') # Find the label
		self.speed = self.findChild(QtWidgets.QLabel, 'SpeedLabel_3') # Find the label
		self.line = self.findChild(QtWidgets.QLabel, 'LineLabel') # Find the label
		self.authority = self.findChild(QtWidgets.QLabel, 'AuthorityLabel_2') # Find the label

		self.RefreshTrainInfo()

		# Automatically refresh Map after 5s
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.RefreshTrainInfo)
		time_timr.start(5000)

	def RefreshTrainInfo(self):
		# If train no longer on tracks
		if(self.tnum not in ctc.train_numbers):
			self.LeaveThis()
			return

		train_ind = ctc.train_numbers.index(self.tnum)

		if ctc.trains_arr[train_ind].line_on == Line.LINE_GREEN:
			try:
				self.line.setText('GREEN')
				self.location.setText(str(ctc.green_route_blocks[ctc.trains_arr[train_ind].index_on_route]))
			except:
				pass
		else:
			try:
				self.line.setText('RED')
				self.location.setText(str(ctc.red_route_blocks[ctc.trains_arr[train_ind].index_on_route]))
			except:
				pass
		try:
			self.speed.setText(str(ctc.trains_arr[train_ind].command_speed))
			self.authority.setText(str(ctc.trains_arr[train_ind].authority))
		except:
			pass


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

		self.maint_mode_green = self.findChild(QtWidgets.QLabel, 'MaintModeGr')

		# Initial Refresh
		self.RefreshMapGreen()

		# Automatically refresh Map after 500ms
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.RefreshMapGreen)
		time_timr.start(500)

		# Find the Blocks
		for i in range(1, 151):
			exec('self.GB%s = self.findChild(QtWidgets.QPushButton, \'G%s\')' % (str(i), str(i)))
			eval('self.GB%s.clicked.connect(partial(self.ToggleBlockGreen, %d))' % (str(i), i))
		# Find the Switches
		for i in range(1, 7):
			exec('self.S%s = self.findChild(QtWidgets.QPushButton, \'SW%s\')' % (str(i), str(i)))
			eval('self.S%s.clicked.connect(partial(self.ToggleSwitchGreen, %d))' % (str(i), i))

	def RefreshMapGreen(self):
		# Get Track Occupancies
		tr_oc = ctc.ReturnOccupancies(Line.LINE_GREEN)
		tr_op = ctc.ReturnClosures(Line.LINE_GREEN)

		for i in range(len(tr_oc)):
			if tr_oc[i] and tr_op[i]:
				try:
					eval('self.GB%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")' % str(i + 1))		# if occupied change block color to yellow
				except:
					pass
			elif not tr_op[i]:
				try:
					eval('self.GB%s.setStyleSheet(\"background-color: rgb(252, 1, 7);\")' % str(i + 1))		# if occupied change block color to yellow
				except:
					pass	
			else:
				try:
					eval('self.GB%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")' % str(i + 1))		# if not occupied, change block color to green
				except:
					pass

		# Get Switch Positions
		sw_pos = ctc.ReturnSwitchPositions(Line.LINE_GREEN)

		wrtxt_arr = ctc.ReturnSwitchPositions(Line.LINE_GREEN)
		for i in range(len(wrtxt_arr)):
			wrtxt = wrtxt_arr[i]
			try:
				eval('self.SW%s.setText(\'%s\')' % (str(i + 1), wrtxt))
			except:
				pass

		# Maintence mode label
		if self.num_blocks_closed_green > 0:
			self.maint_mode_green.setText('!!!! IN MAINTENCENCE MODE !!!!')
		else:
			self.maint_mode_green.setText('')

	def ToggleBlockGreen(self, b_num):
		""" Toggle switch block for maintence mode or not """

		# Close the block if it is open
		if ctc.blocks_green_arr[b_num - 1].open:
			self.num_blocks_closed_green += 1
			ctc.blocks_green_arr[b_num - 1].open = False
			# Altert SW Track
			signals.swtrack_set_block_status.emit(Line.LINE_GREEN, b_num, False)
		else:
			self.num_blocks_closed_green -= 1
			ctc.blocks_green_arr[b_num - 1].open = True
			# Altert SW Track
			signals.swtrack_set_block_status.emit(Line.LINE_GREEN, b_num, True)

		if self.num_blocks_closed_green > 0:
			self.maint_mode_green.setText('!!!! IN MAINTENCENCE MODE !!!!')
		else:
			self.maint_mode_green.setText('')

	def ToggleSwitchGreen(self, s_num):
		""" Toggle switch if block is in maintence mode """
		if self.num_blocks_closed_green > 0:
			if ctc.switches_green_arr[s_num - 1].pointing_to == ctc.switches_green_arr[s_num - 1].less_block:
				# Send High to TC if pointing low
				signals.swtrack_set_switch_position.emit(Line.LINE_GREEN,s_num, True)
			else:
				# Send Low to TC if pointing High
				signals.swtrack_set_switch_position.emit(Line.LINE_GREEN, s_num, False)
		else:
			self.maint_mode_green.setText('Don\'t try to switch; Activate Maint. Mode')

	def LeaveThis(self):
		global time_timr
		time_timr.stop()
		self.returnToMainWindow()

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

		self.maint_mode_red = self.findChild(QtWidgets.QLabel, 'MaintModeRd')

		#initial refresh
		self.RefreshMapRed()
		
		# Automatically refresh Map after 1s
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.RefreshMapRed)
		time_timr.start(1000)

		# Find the Blocks
		for i in range(1, 77):
			exec('self.R%s = self.findChild(QtWidgets.QPushButton, \'RB%s\')' % (str(i), str(i)))
			eval('self.R%s.clicked.connect(partial(self.ToggleBlockRed, %d))' % (str(i), i))

		# Find the Switches
		for i in range(1, 8):
			exec('self.S%s = self.findChild(QtWidgets.QPushButton, \'SW%s\')' % (str(i), str(i)))
			eval('self.S%s.clicked.connect(partial(self.ToggleSwitchRed, %d))' % (str(i), i))

	def RefreshMapRed(self):
		# Get Track Occupancies
		tr_oc = ctc.ReturnOccupancies(Line.LINE_RED)
		tr_op = ctc.ReturnClosures(Line.LINE_RED)

		for i in range(len(tr_oc)):
			if tr_oc[i] and tr_op[i]:
				try:
					eval('self.R%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")' % str(i + 1))		# if occupied change block color to yellow
				except:
					pass
			elif not tr_op[i]:
				try:
					eval('self.R%s.setStyleSheet(\"background-color: rgb(252, 1, 7);\")' % str(i + 1))		# if occupied change block color to yellow
				except:
					pass
			else:
				try:
					eval('self.R%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")' % str(i + 1))		# if not occupied, change block color to green
				except:
					pass

		# Get Switch Positions
		sw_pos = ctc.ReturnSwitchPositions(Line.LINE_RED)

		wrtxt_arr = ctc.ReturnSwitchPositions(Line.LINE_RED)
		for i in range(len(wrtxt_arr)):
			wrtxt = wrtxt_arr[i]
			try:
				eval('self.S%s.setText(\'%s\')' % (str(i + 1), wrtxt))
			except:
				pass

		# Maintence mode label
		if self.num_blocks_closed_red > 0:
			self.maint_mode_red.setText('!!!! IN MAINTENCENCE MODE !!!!')
		else:
			self.maint_mode_red.setText('')

	def ToggleBlockRed(self, b_num):
		""" Toggle switch block for maintence mode or not """

		# Close the block if it is open
		if ctc.blocks_red_arr[b_num - 1].open:
			self.num_blocks_closed_red += 1
			ctc.blocks_red_arr[b_num - 1].open = False
			# Altert SW Track
			signals.swtrack_set_block_status.emit(Line.LINE_RED, b_num, False)
		else:
			self.num_blocks_closed_red -= 1
			ctc.blocks_red_arr[b_num - 1].open = True
			# Altert SW Track
			signals.swtrack_set_block_status.emit(Line.LINE_RED, b_num, True)

		if self.num_blocks_closed_red > 0:
			self.maint_mode_red.setText('!!!! IN MAINTENCENCE MODE !!!!')
		else:
			self.maint_mode_red.setText('')

	def ToggleSwitchRed(self, s_num):
		""" Toggle switch if block is in maintence mode """
		if self.num_blocks_closed_red > 0:
			if ctc.switches_red_arr[s_num - 1].pointing_to == ctc.switches_red_arr[s_num - 1].less_block:
				# Send High to TC if pointing low
				signals.swtrack_set_switch_position.emit(Line.LINE_RED, s_num, True)
			else:
				# Send Low to TC if pointing High
				signals.swtrack_set_switch_position.emit(Line.LINE_RED, s_num, False)
		else:
			self.maint_mode_red.setText('Don\'t try to switch; Activate Maint. Mode')

	#######################################################################################################################################
	#######################################################################################################################################
	# Return to main window from all windows function
	#######################################################################################################################################
	#######################################################################################################################################
	def returnToMainWindow(self):
		uic.loadUi('src/UI/CTC/ctc_main.ui', self)
		self.setWindowTitle("CTC Main Page")

		# For reloading throughput value
		global time_timr

		# In Main Window
		self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
		self.button.clicked.connect(self.LoadScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
		self.button.clicked.connect(self.ExitModule)
		self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
		self.button.clicked.connect(self.CheckAutoMode)
		self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
		self.button.clicked.connect(self.MapMenuWindow)

		self.auto = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
		self.auto.clicked.connect(self.ToggleAutomaicMode)

		self.mode_text = self.findChild(QtWidgets.QLabel, 'automodetext')

		if self.auto_mode:
			self.auto.setChecked(True)

		self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label
		self.ShowThroughput()

		# Automatically refresh Map after 10s
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.ShowThroughput)
		time_timr.start(10000)


	#######################################################################################################################################
	#######################################################################################################################################
	# Toggle for Automatic Mode
	#######################################################################################################################################
	#######################################################################################################################################
	def ToggleAutomaicMode(self):
		self.mode_text.setText('')
		if self.auto.isChecked():
			self.auto_mode = True
		else:
			self.auto_mode = False

	#######################################################################################################################################
	#######################################################################################################################################
	# Exits the Module
	#######################################################################################################################################
	#######################################################################################################################################
	def ExitModule(self):
		global time_timr
		time_timr.stop()

		"""Removes the window from the list"""
		window_list.remove(self)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = CTCUi()
	app.exec_()
