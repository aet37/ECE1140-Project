"""Software Track Controller GUI"""

import os
import threading
from time import sleep
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
from UI.window_manager import window_list

HWTRACK_CONTROLLER_NUMBER = '1'

class SWTrackControllerUi(QtWidgets.QMainWindow):
    """GUI for the track controller module"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/SWTrackController/track_controller.ui', self)

        # All the track controllers and the blocks they control
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

        # Current track controller and block selected
        self.current_track_controller = None
        self.current_block = None

        # Find elements and connect them accordingly
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button')
        logout_button.clicked.connect(self.logout)

        switch_position_button = self.findChild(QtWidgets.QPushButton, 'switch_position_button')
        switch_position_button.setAttribute(Qt.WA_TranslucentBackground)
        switch_position_button.clicked.connect(self.switch_position_button_clicked)

        download_program_button = self.findChild(QtWidgets.QPushButton, 'download_program_button')
        download_program_button.clicked.connect(self.download_program)

        self.track_controller_combo_box = self.findChild(QtWidgets.QComboBox, 'track_controller_combo_box')
        self.block_combo_box = self.findChild(QtWidgets.QComboBox, 'block_combo_box')
        self.block_combo_box.currentIndexChanged.connect(self.block_selected)

        # Add all of the options for the red/green line
        for i in range(0, len(self.green_line_controllers)):
            self.track_controller_combo_box.addItem('Green Line - Controller #{}'.format(i + 1))
        for i in range(0, len(self.red_line_controllers)):
            self.track_controller_combo_box.addItem('Red Line - Controller #{}'.format(i + 1))
        self.track_controller_combo_box.currentIndexChanged.connect(self.track_controller_selected)

        # Select the default
        self.track_controller_combo_box.setCurrentIndex(0)
        self.track_controller_selected()
        self.block_combo_box.setCurrentIndex(0)
        self.block_selected()

        # Flag to indicate we are updating the hardware
        self.updating_hardware = False

        # Update the gui and start the periodic timer
        self.send_gather_data_message()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.send_gather_data_message)
        self.update_timer.start(5000)

        self.show()

    def track_controller_selected(self):
        """Method called when a different track controller is selected"""
        self.current_track_controller = self.track_controller_combo_box.currentText().split('#')[1]

        if 'Red' in self.track_controller_combo_box.currentText():
            self.current_track_controller = str(int(self.current_track_controller) + len(self.green_line_controllers))

        # Update the options in the block combo box
        self.block_combo_box.clear()
        if 'Red' in self.track_controller_combo_box.currentText():
            for block in self.red_line_controllers[int(self.current_track_controller) - 1]:
                self.block_combo_box.addItem("Block #{}".format(block))
        else:
            for block in self.green_line_controllers[int(self.current_track_controller) - len(self.green_line_controllers) - 1]:
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
        if self.current_track_controller == HWTRACK_CONTROLLER_NUMBER:
            self.updating_hardware = True

        for line in open(output_file, 'r'):
            line = line.rstrip('\n')
            request_code, _, data = line.partition(' ')
            request_code = RequestCode[request_code]

            # Add the track controller number if we are starting the download
            if request_code == RequestCode.START_DOWNLOAD:
                data += ' ' + self.current_track_controller

            send_message(request_code, data)

        if self.current_track_controller == HWTRACK_CONTROLLER_NUMBER:
            # Spawn a new thread to gather the responses
            thread = threading.Thread(target=self.collect_download_responses)
            thread.start()

    def collect_download_responses(self):
        """Method called when a program is downloaded to the hw controller"""
        while True:
            response_code, response_data = send_message(RequestCode.HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE)
            if response_code == ResponseCode.SUCCESS:
                if "DOWNLOAD COMPLETE" in response_data:
                    break
            sleep(1)

        # Allow timer events again
        self.updating_hardware = False
        self.download_in_progress = False

    def switch_position_button_clicked(self):
        """Method called when the switch position button is pressed"""
        confirmation = Confirmation("Are you sure you want to change the switch position?")

        if confirmation.exec_():
            switch_position_label = self.findChild(QtWidgets.QLabel, 'switch_position_label')
            current_position = switch_position_label.text()
            message = str(self.current_track_controller) + ' ' + ("0" if current_position == '1' else '1')
            send_message(RequestCode.SWTRACK_GUI_SET_SWITCH_POSITION, message)
            switch_position_label.setText(("0" if current_position == '1' else '1'))

    def send_gather_data_message(self):
        """Method called periodically to send the gather data message to the server"""
        print(self.current_track_controller)
        print(self.current_block)

        if self.updating_hardware:
            print("Updating hardware")
            return

        if (self.current_track_controller is not None) and \
           (self.current_block is not None):
            if self.current_track_controller != HWTRACK_CONTROLLER_NUMBER:
                data = str(self.current_track_controller) + ' ' + str(self.current_block)
                send_message_async(RequestCode.SWTRACK_GUI_GATHER_DATA,
                                   data=data,
                                   callback=self.update_gui_sw)
            else:
                data = str(self.current_track_controller) + ' ' + str(self.current_block)
                send_message_async(RequestCode.HWTRACK_GUI_GATHER_DATA,
                                   data=data,
                                   callback=self.update_gui_hw)

    def update_gui_hw(self, *args):
        """Method called to periodically update the gui when the hw track controller is chosen"""
        # Spawn a new thread to gather the responses
        thread = threading.Thread(target=self.gather_data_from_hw)
        thread.start()

        # Don't let messages to be sent
        self.updating_hardware = True

    def gather_data_from_hw(self):
        """Gets responses from the arduino for each of the messages that were sent"""
        # Get response for each tag
        i = 0
        new_response_data = ''

        try:
            while i < 9:
                if self.download_in_progress:
                    raise Exception()

                response_code, response_data = send_message(RequestCode.HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE)
                if response_code == ResponseCode.SUCCESS:
                    splits = response_data.split(' ')
                    print(splits)
                    if splits[0] == '0':
                        new_response_data += splits[1] + ' '
                    else:
                        new_response_data += '-1' + ' '
                    i += 1
                else:
                    sleep(1)
        except:
            self.updating_hardware = False
            return

        # If we are still looking at the hardware
        if self.current_track_controller == HWTRACK_CONTROLLER_NUMBER:
            self.update_gui_sw(ResponseCode.SUCCESS, new_response_data)

        # Allow messages to be sent again
        self.updating_hardware = False

    def update_gui_sw(self, response_code, response_data):
        """Method called to periodically update the gui"""
        if response_code == ResponseCode.ERROR:
            print("There was a problem communicating with the server")
            return

        # Parse through the response data
        split_data = response_data.split(' ')

        # Track and block attributes
        track_heater_status = int(split_data[0])
        switch_position = int(split_data[1])
        light_status = int(split_data[2])
        occupied = int(split_data[3])
        track_status = int(split_data[4])
        railway_crossing = int(split_data[5])

        track_heater_label = self.findChild(QtWidgets.QLabel, 'track_heater_label')
        if track_heater_status == -1:
            track_heater_label.setText("ERROR")
        else:
            track_heater_label.setText("ON" if bool(track_heater_status) else "OFF")

        switch_position_label = self.findChild(QtWidgets.QLabel, 'switch_position_label')
        if switch_position == -1:
            switch_position_label.setText("ERROR")
        else:
            switch_position_label.setText("1" if bool(switch_position) else "0")

        light_status_label = self.findChild(QtWidgets.QLabel, 'light_status_label')
        if light_status == 0:
            light_status_label.setText("RED")
        elif light_status == 1:
            light_status_label.setText("YELLOW")
        elif light_status == 2:
            light_status_label.setText("GREEN")
        else:
            light_status_label.setText("ERROR")

        occupied_label = self.findChild(QtWidgets.QLabel, 'occupied_label')
        if occupied == -1:
            occupied_label.setText("ERROR")
        else:
            occupied_label.setText("YES" if bool(occupied) else "NO")

        track_status_label = self.findChild(QtWidgets.QLabel, 'track_status_label')
        if track_status == -1:
            track_status_label.setText("ERROR")
        else:
            track_status_label.setText("OK" if bool(track_status) else "CLOSED")

        railway_crossing_label = self.findChild(QtWidgets.QLabel, 'railway_crossing_label')
        if railway_crossing == -1:
            railway_crossing_label.setText("N/A")
        else:
            railway_crossing_label.setText("UP" if bool(railway_crossing) else "DOWN")

        # Train attributes
        authority_label = self.findChild(QtWidgets.QLabel, 'authority_label')
        suggested_speed_label = self.findChild(QtWidgets.QLabel, 'suggested_speed_label')
        command_speed_label = self.findChild(QtWidgets.QLabel, 'command_speed_label')
        if len(split_data) > 6:
            authority = int(split_data[6])
            suggested_speed = int(split_data[7])
            command_speed = int(split_data[8])

            if authority == -1:
                authority_label.setText("ERROR")
            else:
                authority_label.setText("YES" if bool(authority) else "NO")

            if suggested_speed < 0:
                suggested_speed_label.setText("ERROR")
            else:
                suggested_speed_label.setText(str(suggested_speed) + ' MPH')

            if command_speed < 0:
                command_speed_label.setText("ERROR")
            else:
                command_speed_label.setText(str(command_speed) + ' MPH')
        else:
            authority_label.setText("N/A")
            suggested_speed_label.setText("N/A")
            command_speed_label.setText("N/A")

    def logout(self):
        """Method invoked when the logout button is pressed"""
        window_list.remove(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SWTrackControllerUi()
    app.exec_()
