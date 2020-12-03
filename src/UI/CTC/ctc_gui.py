""" File which contains the class for the CTC GUI to run """

import sys
from functools import partial
from PyQt5 import QtWidgets, uic, QtCore
import pandas as pd

from src.CTC.train_system import ctc
from src.common_def import Line
from src.UI.window_manager import window_list
from src.timekeeper import timekeeper
from src.signals import signals
from src.CTC.ctc_def import InterruptTrain

# GLOBALS
class CTCUi(QtWidgets.QMainWindow):
    """ Class which controls CTC GUI """

    # UI Class initializer
    def __init__(self):
        super(CTCUi, self).__init__()
        uic.loadUi('src/UI/CTC/ctc_main.ui', self)

        self.setWindowTitle("CTC Main Page")

        #init
        signals.ctc_update_failure_blocks_gui.connect(self.update_blocks_faliure_numbers)
        self.tnum = -1
        self.auto_mode = False
        self.num_blocks_closed_green = 0
        self.num_blocks_closed_red = 0
        self.open_file = ''

        # For reloading throughput value
        global TIME_TIMR

        # In Main Window
        self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
        self.button.clicked.connect(self.load_schedule_window)
        self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
        self.button.clicked.connect(self.exit_module)
        self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
        self.button.clicked.connect(self.check_auto_mode)
        self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
        self.button.clicked.connect(self.map_menu_window)

        self.auto = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
        self.auto.clicked.connect(self.toggle_automatic_mode)

        self.mode_text = self.findChild(QtWidgets.QLabel, 'automodetext')

        if self.auto_mode:
            self.auto.setChecked(True)

        self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label
        self.show_throughput()

        # Automatically refresh throughput after 5s
        TIME_TIMR = QtCore.QTimer(self)
        TIME_TIMR.timeout.connect(self.show_throughput)
        TIME_TIMR.start(5000)


        self.show()

    def update_blocks_faliure_numbers(self, ln, failure):
        """ Update Maintenece Block counts from CTC """

        if ln ==Line.LINE_GREEN:
            if failure:
                self.num_blocks_closed_green += 1
            else:
                self.num_blocks_closed_green -= 1
        else:
            if failure:
                self.num_blocks_closed_red += 1
            else:
                self.num_blocks_closed_red -= 1

    def show_throughput(self):
        """ Displays Throughput on main screen """

        try:
            self.tplabel.setText(str(ctc.throughput))
            self.mode_text.setText('')
        except:
            pass

    def check_auto_mode(self):
        """ Checks if CTC is in automatic mode to determin if train can be dispatched """

        if self.auto_mode == True:
            self.mode_text.setText('ERROR: Cannot Dispatch in Automatic Mode')
        else:
            self.dispatch_train_window()

    ###############################################################################################
    ###############################################################################################
    # Opens Load Schedule Page
    ###############################################################################################
    ###############################################################################################
    def load_schedule_window(self):
        """ Defines the window to load and run a schedule """

        uic.loadUi('src/UI/CTC/ctc_schedule_import.ui', self)
        self.setWindowTitle("CTC - Load Schedule")

        self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
        self.button.clicked.connect(self.return_to_main_window)

        self.chose_file = self.findChild(QtWidgets.QPushButton, 'ChoseFile') # Find the button
        self.chose_file.clicked.connect(self.chose_a_file)

        self.upload_and_run = self.findChild(QtWidgets.QPushButton, 'UploadAndRun') # Find the butt
        self.upload_and_run.clicked.connect(self.run_schedule)

        self.file_path = self.findChild(QtWidgets.QLabel, 'FilePath') # Find the Label
        self.error_conf = self.findChild(QtWidgets.QLabel, 'ConfErr') # Find the Label

        # Initialize to blank
        self.open_file = ''

    def chose_a_file(self):
        """ Allows user to chose a schedule file """

        dialog = QtWidgets.QFileDialog(self)
        fname = dialog.getOpenFileName(self)

        if fname[0][-5:len(fname[0])] != '.xlsx':
            self.error_conf.setStyleSheet('color: rgb(252, 1, 7);')
            self.error_conf.setText('Please Chose an Excel File!')
        else:
            self.open_file = fname[0]
            self.file_path.setText(self.open_file)
            self.error_conf.setText('')

    def run_schedule(self):
        """ Runs the schedule from the excel file """

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
                self.error_conf.setText('Faulty Excel File. Please Scrupulously \
                    look for error in file.')
                return

        # If passed, add the trains to the time class
        for i in range(len(to_add)):
            timekeeper.ctc_trains_backlog.append(to_add[i])

        # Display Sucess on Screen
        self.file_path.setText('')
        self.open_file = ''
        self.error_conf.setStyleSheet('color: rgb(33, 255, 6);')
        self.error_conf.setText('Sucess! Schedule starting to run...')



    ###############################################################################################
    ###############################################################################################
    # Opens Map Menu Page
    ###############################################################################################
    ###############################################################################################
    def map_menu_window(self):
        """ Window which displays view map and view train options """

        global TIME_TIMR

        uic.loadUi('src/UI/CTC/ctc_map_menu.ui', self)
        self.setWindowTitle("CTC - Map Menu")

        self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # return button
        self.button.clicked.connect(self.leave_this)

        self.trains_label = self.findChild(QtWidgets.QLabel, 'TrainsLabel') # valid train label

        self.button = self.findChild(QtWidgets.QPushButton, 'ViewGreen') # view green button
        self.button.clicked.connect(self.green_map_window)

        self.button = self.findChild(QtWidgets.QPushButton, 'ViewRed') # view red button
        self.button.clicked.connect(self.red_map_window)

        self.train_id_label = self.findChild(QtWidgets.QLineEdit, 'ViewTrainNum') # Train ID
        self.error_label = self.findChild(QtWidgets.QLabel, 'ErrLabel') # Input for Train ID
        self.train_button = self.findChild(QtWidgets.QPushButton, 'ViewTrainButton') # Train Status
        self.train_button.clicked.connect(self.open_if_good)

        self.update_trains_list()

        # Automatically refresh Map after 1s
        TIME_TIMR = QtCore.QTimer(self)
        TIME_TIMR.timeout.connect(self.update_trains_list)
        TIME_TIMR.start(1000)


    def update_trains_list(self):
        """ Updates the train list on the screen with current trains on tracks """

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



    def open_if_good(self):
        """ Opens train informatio window if vaild train nubmer inputed """

        if self.train_id_label.text() == '':
            return
        else:
            try:
                int(self.train_id_label.text())
            except:
                self.error_label.setStyleSheet("color: red")
                self.error_label.setText('Error: Invalid Train Num Entered')
                return

            if int(self.train_id_label.text()) < 1:
                self.error_label.setStyleSheet("color: red")
                self.error_label.setText('Error: Invalid Train Num Entered')
                return

            valid = int(self.train_id_label.text()) in ctc.train_numbers

            if valid:  # If sucessfuly found the train in the system
                self.tnum = int(self.train_id_label.text())
                self.train_info_window()
            else:
                self.error_label.setStyleSheet("color: red")
                self.error_label.setText('Error: Invalid Train Num Entered')

    ###############################################################################################
    ###############################################################################################
    # Opens Dispatch Train Window
    ###############################################################################################
    ###############################################################################################
    def dispatch_train_window(self):
        """ Window which allows user to dispatch a train """

        uic.loadUi('src/UI/CTC/ctc_dispatch_train.ui', self)
        self.setWindowTitle("CTC - Dispatch Train")

        self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
        self.button.clicked.connect(self.return_to_main_window)

        self.green_radio = self.findChild(QtWidgets.QRadioButton, 'GreenRadio')
        self.red_radio = self.findChild(QtWidgets.QRadioButton, 'RedRadio')

        self.d_block_label = self.findChild(QtWidgets.QLineEdit, 'BlockInput') # Find the text inpu
        self.d_time_label = self.findChild(QtWidgets.QLineEdit, 'TimeInput') # Find the input

        self.d_conf_label = self.findChild(QtWidgets.QLabel, 'ConfirmationLabel') # Find the label
        self.d_speed_label = self.findChild(QtWidgets.QLabel, 'SpeedOut') # Find the label
        self.d_auth_label = self.findChild(QtWidgets.QLabel, 'AuthorityOut') # Find the label

        self.button = self.findChild(QtWidgets.QPushButton, 'DispatchButton') # Find the button
        self.button.clicked.connect(self.dispatch_train)


    def dispatch_train(self):
        """ Dispatches a train once user clicks button """

        # If simulation paused, dont let dispatch
        if timekeeper.paused:
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: simulation paused')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return

        # Red line
        if self.red_radio.isChecked() and len(self.d_time_label.text()) == 0:
            if ctc.blocks_red_arr[8].occupied:
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Wait until train leaves block 9')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return
            for i in range(len(ctc.trains_arr)):
                if ctc.trains_arr[i].line_on == Line.LINE_RED and\
                ctc.trains_arr[i].index_on_route == 0:
                    self.d_conf_label.setStyleSheet("color: red")
                    self.d_conf_label.setText('Wait until Previous train leaves Yard')
                    self.d_speed_label.setText('')
                    self.d_auth_label.setText('')
                    return

        # Green Line
        elif len(self.d_time_label.text()) == 0:
            if ctc.blocks_green_arr[61].occupied or ctc.blocks_green_arr[60].occupied:
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Wait until train leaves block 62 or 61')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return
            for i in range(len(ctc.trains_arr)):
                if ctc.trains_arr[i].line_on == Line.LINE_GREEN and\
                ctc.trains_arr[i].index_on_route == 0:
                    self.d_conf_label.setStyleSheet("color: red")
                    self.d_conf_label.setText('Wait until Previous train leaves Yard')
                    self.d_speed_label.setText('')
                    self.d_auth_label.setText('')
                    return

        # Error Check block value
        try:
            int(self.d_block_label.text())
        except:
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: Invalid Block Entered')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return

        # Make sure user specified a line
        if not self.green_radio.isChecked() and not self.red_radio.isChecked():
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: Please Select a Line')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return

        # Error Check for block value
        if int(self.d_block_label.text()) <= 0 or len(self.d_block_label.text()) == 0:
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: Invalid Block Entered')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return
        elif self.red_radio.isChecked() and int(self.d_block_label.text()) > 76:
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: Invalid Block Entered For Red Line')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return
        elif self.red_radio.isChecked() == False and int(self.d_block_label.text()) > 155:
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: Invalid Block Entered For Green Line')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return

        # Error Check for time value
        if len(self.d_time_label.text()) != 6 and len(self.d_time_label.text()) != 0:
            self.d_conf_label.setStyleSheet("color: red")
            self.d_conf_label.setText('Error: Invalid Time Entered 3')
            self.d_speed_label.setText('')
            self.d_auth_label.setText('')
            return
        elif len(self.d_time_label.text()) == 6:

            # Error Check time values
            try:
                int(self.d_time_label.text()[0] + self.d_time_label.text()[1])
            except:
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Error: Invalid Time Entered 1')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return
            try:
                int(self.d_time_label.text()[3] + self.d_time_label.text()[4])
            except:
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Error: Invalid Time Entered 2')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return

            if int(self.d_time_label.text()[0] + self.d_time_label.text()[1]) not in range(1, 13):
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Error: Invalid Time Entered 4')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return
            elif int(self.d_time_label.text()[3] + self.d_time_label.text()[4]) not in range(60):
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Error: Invalid Time Entered 5')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return
            elif self.d_time_label.text()[5] not in ['a', 'p']:
                self.d_conf_label.setStyleSheet("color: red")
                self.d_conf_label.setText('Error: Invalid Time of Day  Entered (a/p)')
                self.d_speed_label.setText('')
                self.d_auth_label.setText('')
                return

            # Print confirmation to screen and take actions if information valid
            else:
                self.d_conf_label.setStyleSheet("color: green")
                self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text()\
                    + ' at ' + self.d_time_label.text())
                self.d_speed_label.setText('Command Speed [to Track Controller]: 43 MPH')
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
                    temp_time_train = InterruptTrain(int(self.d_block_label.text()),\
                        Line.LINE_RED, hr, minute)
                else:
                    temp_time_train = InterruptTrain(int(self.d_block_label.text()),\
                        Line.LINE_GREEN, hr, minute)

                # Add the train to the interrupt list
                timekeeper.ctc_trains_backlog.append(temp_time_train)
        else:
            self.d_conf_label.setStyleSheet("color: green")
            self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text()\
                + ' Now')
            self.d_speed_label.setText('Command Speed [to Track Controller]: 43 MPH')
            self.d_auth_label.setText('Authority [to Track Controller]: 3 Blocks')
            if self.red_radio.isChecked():
                ctc.dispatch_train(int(self.d_block_label.text()), Line.LINE_RED)
            else:
                ctc.dispatch_train(int(self.d_block_label.text()), Line.LINE_GREEN)

    ###############################################################################################
    ###############################################################################################
    # Opens Train Information Window
    ###############################################################################################
    ###############################################################################################
    def train_info_window(self):
        """ Window which provides information about a train """

        global TIME_TIMR
        uic.loadUi('src/UI/CTC/ctc_view_train.ui', self)
        self.setWindowTitle("CTC - View Train Info")

        self.button = self.findChild(QtWidgets.QPushButton, 'BackToMapMenu') # Find the button
        self.button.clicked.connect(self.leave_this)

        self.location = self.findChild(QtWidgets.QLabel, 'BlockLabel') # Find the label
        self.speed = self.findChild(QtWidgets.QLabel, 'SpeedLabel_3') # Find the label
        self.line = self.findChild(QtWidgets.QLabel, 'LineLabel') # Find the label
        self.authority = self.findChild(QtWidgets.QLabel, 'AuthorityLabel_2') # Find the label

        self.refresh_train_info()

        # Automatically refresh Map after 0.7s
        TIME_TIMR = QtCore.QTimer(self)
        TIME_TIMR.timeout.connect(self.refresh_train_info)
        TIME_TIMR.start(700)

    def refresh_train_info(self):
        """ Refreshes the infomration on the train window page """

        # If train no longer on tracks
        if self.tnum not in ctc.train_numbers:
            self.leave_this()
            return

        train_ind = ctc.train_numbers.index(self.tnum)

        if ctc.trains_arr[train_ind].line_on == Line.LINE_GREEN:
            try:
                self.line.setText('GREEN')
                self.location.setText(str(ctc.green_route_blocks[ctc.trains_arr[train_ind]\
                    .index_on_route]))
            except:
                pass
        else:
            try:
                self.line.setText('RED')
                self.location.setText(str(ctc.red_route_blocks[ctc.trains_arr[train_ind]\
                    .index_on_route]))
            except:
                pass
        try:
            self.speed.setText(str(ctc.trains_arr[train_ind].command_speed / 1.609))
            self.authority.setText(str(ctc.trains_arr[train_ind].authority))
        except:
            pass


    ###############################################################################################
    ###############################################################################################
    # Opens Green Map Window
    ###############################################################################################
    ###############################################################################################
    def green_map_window(self):
        """ Window which displays the green line and information about it """

        global TIME_TIMR
        uic.loadUi('src/UI/CTC/ctc_view_green_line.ui', self)
        self.setWindowTitle("CTC - View Green Map")

        self.button = self.findChild(QtWidgets.QPushButton, 'BackToMapMenu') # Find the button
        self.button.clicked.connect(self.leave_this)

        self.maint_mode_green = self.findChild(QtWidgets.QLabel, 'MaintModeGr')

        # Initial Refresh
        self.refresh_map_green()

        # Automatically refresh Map after 500ms
        TIME_TIMR = QtCore.QTimer(self)
        TIME_TIMR.timeout.connect(self.refresh_map_green)
        TIME_TIMR.start(500)

        # Find the Blocks
        for i in range(1, 151):
            exec('self.GB%s = self.findChild(QtWidgets.QPushButton, \'G%s\')' % (str(i), str(i)))
            eval('self.GB%s.clicked.connect(partial(self.toggle_blocks_green, %d))' % (str(i), i))
        # Find the Switches
        for i in range(1, 7):
            exec('self.SG%s = self.findChild(QtWidgets.QPushButton, \'SW%s\')' % (str(i), str(i)))
            eval('self.SG%s.clicked.connect(partial(self.toggle_switch_green, %d))' % (str(i), i))

    def refresh_map_green(self):
        """ Refreshes the green map """

        # Get Track Occupancies
        tr_oc = ctc.return_occupancies(Line.LINE_GREEN)
        tr_op = ctc.return_closures(Line.LINE_GREEN)

        for i in range(len(tr_oc)):
            if tr_oc[i] and tr_op[i]:
                try:
                    eval('self.GB%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")'\
                        % str(i + 1))      # if occupied change block color to yellow
                except:
                    pass
            elif not tr_op[i]:
                try:
                    eval('self.GB%s.setStyleSheet(\"background-color: rgb(252, 1, 7);\")'\
                        % str(i + 1))     # if occupied change block color to yellow
                except:
                    pass
            else:
                try:
                    eval('self.GB%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")'\
                        % str(i + 1))      # if not occupied, change block color to green
                except:
                    pass

        # Get Switch Positions
        wrtxt_arr = ctc.return_switch_positions(Line.LINE_GREEN)

        for i in range(len(wrtxt_arr)):
            wrtxt = wrtxt_arr[i]
            try:
                eval('self.SG%s.setText(\'%s\')' % (str(i + 1), wrtxt))
            except:
                pass

        # Maintence mode label
        if self.num_blocks_closed_green > 0:
            self.maint_mode_green.setText('!!!! IN MAINTENCENCE MODE !!!!')
        else:
            self.maint_mode_green.setText('')

    def toggle_blocks_green(self, b_num):
        """ Toggle switch block for maintence mode or not """

        # If simulation is paused, do nothing
        if timekeeper.paused:
            self.maint_mode_green.setText('Error: Simulation PAUSED')
            return

        # Close the block if it is open
        if ctc.blocks_green_arr[b_num - 1].open:
            signals.swtrack_set_block_status.emit(Line.LINE_GREEN, b_num, True,\
                ctc.blocks_green_arr[b_num - 1].num_faliures)
        else:
            # Altert SW Track
            signals.swtrack_set_block_status.emit(Line.LINE_GREEN, b_num, False,\
                ctc.blocks_green_arr[b_num - 1].num_faliures)

        if self.num_blocks_closed_green > 0:
            self.maint_mode_green.setText('!!!! IN MAINTENCENCE MODE !!!!')
        else:
            self.maint_mode_green.setText('')

    def toggle_switch_green(self, s_num):
        """ Toggle switch if block is in maintence mode """

        # If simulation is paused, do nothing
        if timekeeper.paused:
            self.maint_mode_green.setText('Error: Simulation PAUSED')
            return

        if self.num_blocks_closed_green > 0:
            if ctc.switches_green_arr[s_num - 1].pointing_to == ctc.switches_green_arr\
            [s_num - 1].less_block:
                # Send High to TC if pointing low
                signals.swtrack_set_switch_position.emit(Line.LINE_GREEN,s_num, True)
            else:
                # Send Low to TC if pointing High
                signals.swtrack_set_switch_position.emit(Line.LINE_GREEN, s_num, False)
        else:
            self.maint_mode_green.setText('Don\'t try to switch; Activate Maint. Mode')

    def leave_this(self):
        """ Stops the refresh timer and goes to the main screen """

        global TIME_TIMR
        TIME_TIMR.stop()
        self.return_to_main_window()

    ###############################################################################################
    ###############################################################################################
    # Opens Red Map Window
    ###############################################################################################
    ###############################################################################################
    def red_map_window(self):
        """ Window with map of red line """

        global TIME_TIMR
        uic.loadUi('src/UI/CTC/ctc_view_red_line.ui', self)
        self.setWindowTitle("CTC - View Red Map")

        self.button = self.findChild(QtWidgets.QPushButton, 'BackToMapMenu') # Find the button
        self.button.clicked.connect(self.leave_this)

        self.maint_mode_red = self.findChild(QtWidgets.QLabel, 'MaintModeRd')

        #initial refresh
        self.refresh_map_red()

        # Automatically refresh Map after 1s
        TIME_TIMR = QtCore.QTimer(self)
        TIME_TIMR.timeout.connect(self.refresh_map_red)
        TIME_TIMR.start(1000)

        # Find the Blocks
        for i in range(1, 77):
            exec('self.R%s = self.findChild(QtWidgets.QPushButton, \'RB%s\')' % (str(i), str(i)))
            eval('self.R%s.clicked.connect(partial(self.toggle_block_red, %d))' % (str(i), i))

        # Find the Switches
        for i in range(1, 8):
            exec('self.S%s = self.findChild(QtWidgets.QPushButton, \'SW%s\')' % (str(i), str(i)))
            eval('self.S%s.clicked.connect(partial(self.toggle_switch_red, %d))' % (str(i), i))

    def refresh_map_red(self):
        """ Refreshes the map of the red line """

        # Get Track Occupancies
        tr_oc = ctc.return_occupancies(Line.LINE_RED)
        tr_op = ctc.return_closures(Line.LINE_RED)

        for i in range(len(tr_oc)):
            if tr_oc[i] and tr_op[i]:
                try:
                    eval('self.R%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")'\
                        % str(i + 1))       # if occupied change block color to yellow
                except:
                    pass
            elif not tr_op[i]:
                try:
                    eval('self.R%s.setStyleSheet(\"background-color: rgb(252, 1, 7);\")'\
                        % str(i + 1))      # if occupied change block color to yellow
                except:
                    pass
            else:
                try:
                    eval('self.R%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")'\
                        % str(i + 1))       # if not occupied, change block color to green
                except:
                    pass

        # Get Switch Positions
        wrtxt_arr = ctc.return_switch_positions(Line.LINE_RED)

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

    def toggle_block_red(self, b_num):
        """ Toggle switch block for maintence mode or not on red line """

        # If simulation is paused, do nothing
        if timekeeper.paused:
            self.maint_mode_red.setText('Error: Simulation PAUSED')
            return

        # Close the block if it is open
        if ctc.blocks_red_arr[b_num - 1].open:
            signals.swtrack_set_block_status.emit(Line.LINE_RED, b_num, True,\
                ctc.blocks_red_arr[b_num - 1].num_faliures)
        else:
            # Altert SW Track
            signals.swtrack_set_block_status.emit(Line.LINE_RED, b_num, False,\
                ctc.blocks_red_arr[b_num - 1].num_faliures)

        if self.num_blocks_closed_red > 0:
            self.maint_mode_red.setText('!!!! IN MAINTENCENCE MODE !!!!')
        else:
            self.maint_mode_red.setText('')

    def toggle_switch_red(self, s_num):
        """ Toggle switch if block is in maintence mode on red line"""

        # If simulation is paused, do nothing
        if timekeeper.paused:
            self.maint_mode_red.setText('Error: Simulation PAUSED')
            return

        if self.num_blocks_closed_red > 0:
            if ctc.switches_red_arr[s_num - 1].pointing_to == ctc.switches_red_arr[s_num - 1]\
            .less_block:
                # Send High to TC if pointing low
                signals.swtrack_set_switch_position.emit(Line.LINE_RED, s_num, True)
            else:
                # Send Low to TC if pointing High
                signals.swtrack_set_switch_position.emit(Line.LINE_RED, s_num, False)
        else:
            self.maint_mode_red.setText('Don\'t try to switch; Activate Maint. Mode')

    ###############################################################################################
    ###############################################################################################
    # Return to main window from all windows function
    ###############################################################################################
    ###############################################################################################
    def return_to_main_window(self):
        """ Reinitialize the main window so that user can return to it """

        uic.loadUi('src/UI/CTC/ctc_main.ui', self)
        self.setWindowTitle("CTC Main Page")

        # For reloading throughput value
        global TIME_TIMR

        # In Main Window
        self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
        self.button.clicked.connect(self.load_schedule_window)
        self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
        self.button.clicked.connect(self.exit_module)
        self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
        self.button.clicked.connect(self.check_auto_mode)
        self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
        self.button.clicked.connect(self.map_menu_window)

        self.auto = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
        self.auto.clicked.connect(self.toggle_automatic_mode)

        self.mode_text = self.findChild(QtWidgets.QLabel, 'automodetext')

        if self.auto_mode:
            self.auto.setChecked(True)

        self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label
        self.show_throughput()

        # Automatically refresh trhoughput after 5s
        TIME_TIMR = QtCore.QTimer(self)
        TIME_TIMR.timeout.connect(self.show_throughput)
        TIME_TIMR.start(5000)


    ###############################################################################################
    ###############################################################################################
    # Toggle for Automatic Mode
    ###############################################################################################
    ###############################################################################################
    def toggle_automatic_mode(self):
        """ Toggles automatic mode """

        self.mode_text.setText('')

        if timekeeper.paused:
            self.mode_text.setText('Error: Simulation Paused')
            self.auto.setChecked(self.auto_mode)
            return

        if self.auto.isChecked():
            self.auto_mode = True
        else:
            self.auto_mode = False

    ###############################################################################################
    ###############################################################################################
    # Exits the Module
    ###############################################################################################
    ###############################################################################################
    def exit_module(self):
        """ Closes CTC UI upon stopping refresh timer """

        global TIME_TIMR
        TIME_TIMR.stop()

        """Removes the window from the list"""
        window_list.remove(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CTCUi()
    app.exec_()
