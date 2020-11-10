"""Software Track Controller GUI"""

import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QTimer

sys.path.insert(1, 'src')
from SWTrackController.Compiler.lexer import CompilationError, Lexer
from SWTrackController.Compiler.emitter import Emitter
from SWTrackController.Compiler.parse import Parser

from UI.server_functions import RequestCode, ResponseCode, send_message, send_message_async

from UI.Common.common import Alert, Confirmation

class SWTrackControllerUi(QtWidgets.QMainWindow):
    """GUI for the track controller module"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/SWTrackController/track_controller.ui', self)

        # All the track controllers and the blocks they control
        self.red_line_controllers = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9], # Switch between C and D @ block 9
            [0, 9, 10, 11, 12, 13, 14, 15],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], # Switch between A, E, and F @ block 16
            [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], # Switch between H and T @ block 27
            [72, 73, 74, 75, 76, 27, 28, 29, 30, 31, 32],
            [72, 73, 74, 75, 76, 28, 29, 30, 31, 32, 33], # Switch between R and H @ block 33
            [33, 34, 35, 36, 37],
            [34, 35, 36, 37, 38], # Switch between H and Q @ block 38
            [38, 39, 40, 41, 42, 43, 71, 70, 69, 68, 67],
            [39, 40, 41, 42, 43, 44, 71, 70, 69, 68, 67], # Switch between O and H @ block 44
            [44, 45, 46, 47, 48, 49, 50, 51],
            [45, 46, 47, 48, 49, 50, 51, 52], # Switch between J and N @ block 52
            [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]
        ]

        self.green_line_controllers = [
            [0, 62, 61, 60, 59], # Switch between J, K, and Yard @ block 62
            [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76],
            [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 101] + list(range(102, 151)), # Switch between M, N, and R @ block 77
            [77, 78, 79, 80, 81, 82, 83, 84],
            [85, 78, 79, 80, 81, 82, 83, 84], # Switch between N, O, and Q @ block 85
            [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
            list(range(101, 151)) + list(range(29, 58)), # Switch between Z, F, and G @ block 29
            [29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14],
            [28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13], # Switch between D, A, and C @ block 13
            [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            list(range(30, 59)), # Switch between I, J and Yard @ block 58
            [58, 59, 60, 61]
        ]

        # Current track controller and block selected
        self.current_track_controller = None
        self.current_block = None

        # Find elements and connect them accordingly
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button')
        logout_button.clicked.connect(SWTrackControllerUi.logout)

        switch_position_button = self.findChild(QtWidgets.QPushButton, 'switch_position_button')
        switch_position_button.setAttribute(Qt.WA_TranslucentBackground)
        switch_position_button.clicked.connect(self.switch_position_button_clicked)

        download_program_button = self.findChild(QtWidgets.QPushButton, 'download_program_button')
        download_program_button.clicked.connect(self.download_program)

        self.track_controller_combo_box = self.findChild(QtWidgets.QComboBox, 'track_controller_combo_box')
        self.block_combo_box = self.findChild(QtWidgets.QComboBox, 'block_combo_box')
        self.block_combo_box.currentIndexChanged.connect(self.block_selected)

        # Add all of the options for the red/green line
        for i in range(0, len(self.red_line_controllers)):
            self.track_controller_combo_box.addItem('Red Line - Controller #{}'.format(i + 1))
        for i in range(0, len(self.green_line_controllers)):
            self.track_controller_combo_box.addItem('Green Line - Controller #{}'.format(i + 1))
        self.track_controller_combo_box.currentIndexChanged.connect(self.track_controller_selected)

        # Select the default
        self.track_controller_combo_box.setCurrentIndex(0)
        self.track_controller_selected()
        self.block_combo_box.setCurrentIndex(0)
        self.block_selected()

        # Update the gui and start the periodic timer
        self.send_gather_data_message()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.send_gather_data_message)
        self.update_timer.start(5000)

        self.show()

    def track_controller_selected(self):
        """Method called when a different track controller is selected"""
        self.current_track_controller = self.track_controller_combo_box.currentText().split('#')[1]

        if 'Green' in self.track_controller_combo_box.currentText():
            self.current_track_controller = str(int(self.current_track_controller) + len(self.red_line_controllers))

        # Update the options in the block combo box
        self.block_combo_box.clear()
        if 'Red' in self.track_controller_combo_box.currentText():
            for block in self.red_line_controllers[int(self.current_track_controller) - 1]:
                self.block_combo_box.addItem("Block #{}".format(block))
        else:
            for block in self.green_line_controllers[int(self.current_track_controller) - len(self.red_line_controllers) - 1]:
                self.block_combo_box.addItem("Block #{}".format(block))

    def block_selected(self):
        """Method called when a different block is selected"""
        try:
            self.current_block = self.block_combo_box.currentText().split('#')[1]
        except IndexError:
            self.current_block = None

    def download_program(self):
        """Method called when the download program button is pressed"""
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setWindowTitle("Select Program to Download")
        dialog.setNameFilter("Text files (*.txt)")

        # Return if the user hits cancel
        if not dialog.exec_():
            return

        file_name = dialog.selectedFiles()
        output_file = self.compile_program(file_name[0])

        if output_file is not None:
            self.send_compiled_program(output_file)
            alert = Alert("Program downloaded successfully!")
            alert.exec_()

    @staticmethod
    def compile_program(file_name):
        """Method used to invoke the PLC language compiler on the given file

        :param str file_name: Absolute path to the file to compile

        :return: Name of the output file. None if compilation failed
        """
        # Gather the source code from the file
        source_code = ''
        for line in open(file_name, 'r'):
            source_code = ''.join([source_code, line])

        # Create compiler elements
        output_file = 'CompiledOutput.txt'
        lex = Lexer(source_code)
        emitter = Emitter(output_file)
        par = Parser(lex, emitter)

        # Try to compile
        try:
            par.program(program_name=os.path.splitext(os.path.basename(file_name))[0])
            return output_file
        except CompilationError as compilation_error:
            alert = Alert("Compilation failed with error:\n {}".format(str(compilation_error)))
            alert.exec_()
            return None

    def send_compiled_program(self, output_file):
        """Method used to read compiled program and send messages to the server

        :param str output_file: Name of the file containing the compiled program
        """
        for line in open(output_file, 'r'):
            line = line.rstrip('\n')
            request_code, _, data = line.partition(' ')
            request_code = RequestCode[request_code]

            # Add the track controller number if we are starting the download
            if request_code == RequestCode.START_DOWNLOAD:
                data += ' ' + self.current_track_controller

            send_message(request_code, data)

    def switch_position_button_clicked(self):
        """Method called when the switch position button is pressed"""
        confirmation = Confirmation("Are you sure you want to change the switch position?")

        if confirmation.exec_():
            switch_position_label = self.findChild(QtWidgets.QLabel, 'switch_position_label')
            current_position = switch_position_label.text()
            message = str(self.current_track_controller) + ' ' + ("0" if current_position == '1' else '1')
            send_message(RequestCode.SWTRACK_GUI_SET_SWITCH_POSITION, message)

    def send_gather_data_message(self):
        """Method called periodically to send the gather data message to the server"""
        print(self.current_track_controller)
        print(self.current_block)

        if (self.current_track_controller is not None) and \
           (self.current_block is not None):
            data = str(self.current_track_controller) + ' ' + str(self.current_block)
            send_message_async(RequestCode.SWTRACK_GUI_GATHER_DATA,
                               data=data,
                               callback=self.update_gui)

    def update_gui(self, response_code, response_data):
        """Method called to periodically update the gui"""
        if response_code == ResponseCode.ERROR:
            print("There was a problem communicating with the server")
            return

        # Parse through the response data
        split_data = response_data.split(' ')

        # Track and block attributes
        track_heater_status = bool(split_data[0])
        switch_position = bool(split_data[1])
        light_status = int(split_data[2])
        occupied = bool(split_data[3])
        track_status = int(split_data[4])
        railway_crossing = int(split_data[5])

        track_heater_label = self.findChild(QtWidgets.QLabel, 'track_heater_label')
        track_heater_label.setText("ON" if track_heater_status else "OFF")

        switch_position_label = self.findChild(QtWidgets.QLabel, 'switch_position_label')
        switch_position_label.setText("1" if switch_position else "0")

        light_status_label = self.findChild(QtWidgets.QLabel, 'light_status_label')
        if light_status == 0:
            light_status_label.setText("N/A")
        elif light_status == 1:
            light_status_label.setText("RED")
        else:
            light_status_label.setText("GREEN")

        occupied_label = self.findChild(QtWidgets.QLabel, 'occupied_label')
        occupied_label.setText("YES" if occupied else "NO")

        track_status_label = self.findChild(QtWidgets.QLabel, 'track_status_label')
        track_status_label.setText("OK" if track_status != 0 else "CLOSED")

        railway_crossing_label = self.findChild(QtWidgets.QLabel, 'railway_crossing_label')
        railway_crossing_label.setText("N/A" if railway_crossing == 0 else "DOWN")

        # Train attributes
        if len(split_data > 6):
            authority = bool(split_data[6])
            suggest_speed = int(split_data[7])
            command_speed = int(split_data[8])

            authority_label = self.findChild(QtWidgets.QLabel, 'authority_label')
            authority_label.setText("YES" if authority else "NO")

            suggest_speed_label = self.findChild(QtWidgets.QLabel, 'suggest_speed_label')
            suggest_speed_label.setText(str(suggest_speed) + ' MPH')

            command_speed_label = self.findChild(QtWidgets.QLabel, 'command_speed_label')
            command_speed_label.setText(str(command_speed) + ' MPH')

    @staticmethod
    def logout():
        """Method invoked when the logout button is pressed"""
        if sys.platform == 'darwin':
            os.system('python3 src/UI/login_gui.py &')
        else:
            os.system('start /B python src/UI/login_gui.py')
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = SWTrackControllerUi()
app.exec_()
