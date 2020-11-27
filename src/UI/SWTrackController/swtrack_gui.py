"""Software Track Controller GUI"""

import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from src.SWTrackController.Compiler.lexer import CompilationError, Lexer
from src.SWTrackController.Compiler.emitter import Emitter
from src.SWTrackController.Compiler.parse import Parser

from src.UI.Common.common import Alert, Confirmation
from src.UI.window_manager import window_list
from src.signals import signals
from src.common_def import Line
from src.SWTrackController.track_system import track_system
from src.logger import get_logger

logger = get_logger(__name__)

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

        self.track_heater_label = self.findChild(QtWidgets.QLabel, 'track_heater_label')
        self.switch_position_label = self.findChild(QtWidgets.QLabel, 'switch_position_label')
        self.light_status_label = self.findChild(QtWidgets.QLabel, 'light_status_label')
        self.occupied_label = self.findChild(QtWidgets.QLabel, 'occupied_label')
        self.block_status_label = self.findChild(QtWidgets.QLabel, 'block_status_label')
        self.railway_crossing_label = self.findChild(QtWidgets.QLabel, 'railway_crossing_label')
        self.authority_label = self.findChild(QtWidgets.QLabel, 'authority_label')
        self.suggested_speed_label = self.findChild(QtWidgets.QLabel, 'suggested_speed_label')
        self.command_speed_label = self.findChild(QtWidgets.QLabel, 'command_speed_label')

        # switch_position_button = self.findChild(QtWidgets.QPushButton, 'switch_position_button')
        # switch_position_button.setAttribute(Qt.WA_TranslucentBackground)
        # switch_position_button.clicked.connect(self.switch_position_button_clicked)

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

        # Connect to signals
        signals.swtrack_update_gui.connect(self.update_gui)

        self.show()

    def track_controller_selected(self):
        """Method called when a different track controller is selected"""
        self.current_track_controller = int(self.track_controller_combo_box.currentText().split('#')[1])

        if 'Red' in self.track_controller_combo_box.currentText():
            self.current_track_controller = int(self.current_track_controller) + len(self.green_line_controllers)

        # Update the options in the block combo box
        self.block_combo_box.clear()
        if 'Red' in self.track_controller_combo_box.currentText():
            for block in self.red_line_controllers[self.current_track_controller - 1]:
                self.block_combo_box.addItem("Block #{}".format(block))
        else:
            for block in self.green_line_controllers[self.current_track_controller - len(self.green_line_controllers) - 1]:
                self.block_combo_box.addItem("Block #{}".format(block))

        # Update gui since a new track controller was selected
        self.update_gui()

    def block_selected(self):
        """Method called when a different block is selected"""
        try:
            self.current_block = self.block_combo_box.currentText().split('#')[1]
        except IndexError:
            self.current_block = None

        # Update gui since a new block was selected
        self.update_gui()

    def update_gui(self):
        """Updates the information in the gui using the currently selected
        track controller and block
        """
        logger.info("Updating track controller gui")

        # Get the correct track controller
        if 'Red' in self.track_controller_combo_box.currentText():
            line = Line.LINE_RED
            track_controller = track_system.red_track_controllers[self.current_track_controller - 1]
        else:
            line = Line.LINE_GREEN
            track_controller = track_system.green_track_controllers[self.current_track_controller - 1]

        # Track heater label
        track_heater_status = track_controller.get_track_heater_status()
        self.track_heater_label.setText(self.determine_text(track_heater_status, "ON", "OFF"))

        # Switch Position
        switch_position = track_controller.get_switch_position()
        self.switch_position_label.setText(self.determine_text(switch_position, "0", "1"))

        # Light status
        light_status = track_controller.get_light_status()
        self.light_status_label.setText(self.determine_text(light_status, "GREEN", "RED"))

        # Occupied
        occupied = track_controller.get_block_occupancy(self.current_block)
        self.occupied_label.setText(self.determine_text(occupied, "YES", "NO"))

        # Block status
        block_status = track_controller.get_block_status(self.current_block)
        self.block_status_label.setText(self.determine_text(block_status, "OK", "CLOSED"))

        # Railway crossing
        railway_crossing = track_controller.get_railway_crossing(self.current_block)
        self.railway_crossing_label.setText(self.determine_text(railway_crossing, "DOWN", "UP"))

        if occupied:
            # Authority
            authority = track_controller.get_authority_of_block(self.current_block)
            self.authority_label.setText("YES" if authority else "NO")

            # Suggested Speed
            self.suggested_speed_label.setText("55 MPH")

            # Command Speed
            speed_limit = track_system.get_speed_limit_of_block(line, self.current_block)
            if speed_limit < 55.0:
                self.command_speed_label.setText("{} MPH".format(speed_limit))
            else:
                self.command_speed_label.setText("55 MPH")
        else:
            self.authority_label.setText("-")
            self.suggested_speed_label.setText("-")
            self.command_speed_label.setText("-")

    @staticmethod
    def determine_text(tag_value, true_text, false_text):
        """Given the tag value, returns what to display"""
        if tag_value is None:
            return "-"
        elif tag_value:
            return true_text
        elif not tag_value:
            return false_text
        else:
            assert False, "Unexpected tag value"

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

        self.update_gui()

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
        """Method used to download the compiled program to the currently selected
        track controller instance

        :param str output_file: Name of the file containing the compiled program
        """
        if 'Red' in self.track_controller_combo_box.currentText():
            track_controller = track_system.red_track_controllers[self.current_track_controller - 1]
        else:
            track_controller = track_system.green_track_controllers[self.current_track_controller - 1]

        track_controller.download_program(output_file)

    def switch_position_button_clicked(self):
        """Method called when the switch position button is pressed"""
        confirmation = Confirmation("Are you sure you want to change the switch position?")

        if confirmation.exec_():
            pass
            # TODO(ljk): Emit signal for this

    def logout(self):
        """Method invoked when the logout button is pressed"""
        self.close()
        window_list.remove(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SWTrackControllerUi()
    app.exec_()
