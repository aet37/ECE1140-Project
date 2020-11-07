"""Software Track Controller GUI"""

import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

sys.path.insert(1, 'src')
from SWTrackController.Compiler.lexer import CompilationError, Lexer
from SWTrackController.Compiler.emitter import Emitter
from SWTrackController.Compiler.parse import Parser

from UI.server_functions import RequestCode, send_message

from UI.Common.common import Alert

class SWTrackControllerUi(QtWidgets.QMainWindow):
    """GUI for the track controller module"""
    def __init__(self):
        super().__init__()
        uic.loadUi('src/UI/SWTrackController/track_controller.ui', self)

        # Current track controller and block selected
        self.current_track_controller = None
        self.current_block = None

        # Find elements and connect them accordingly
        logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button')
        logout_button.clicked.connect(SWTrackControllerUi.logout)

        download_program_button = self.findChild(QtWidgets.QPushButton, 'download_program_button')
        download_program_button.clicked.connect(self.download_program)

        self.show()

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

    @staticmethod
    def send_compiled_program(output_file):
        """Method used to read compiled program and send messages to the server

        :param str output_file: Name of the file containing the compiled program
        """
        for line in open(output_file, 'r'):
            line = line.rstrip('\n')
            request_code, _, data = line.partition(' ')
            request_code = RequestCode[request_code]

            send_message(request_code, data)

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
