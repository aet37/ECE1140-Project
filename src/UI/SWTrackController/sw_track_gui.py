
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys

sys.path.insert(1, 'src')
from SWTrackController.Compiler.lexer import Lexer
from SWTrackController.Compiler.emitter import Emitter
from SWTrackController.Compiler.parse import Parser

class SWTrackControllerUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SWTrackControllerUi, self).__init__()
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
        self.compile_program(file_name[0])

    def compile_program(self, file_name):
        """Method used to invoke the PLC language compiler on the given file

        :param str file_name: Absolute path to the file to compile

        :return: Name of the output file. None if compilation failed
        """
        # Gather the source code from the file
        source_code = ''
        for line in open(file_name, 'r'):
            source_code += line

        # Create compiler elements
        lex = Lexer(source_code)
        emitter = Emitter("CompiledOutput.txt")
        par = Parser(lex, emitter)

        # Try to compile
        try:
            par.program()
        except:
            print("Compilation failed!")

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