"""Main file to run"""

from argparse import ArgumentParser
import sys
from PyQt5 import QtWidgets

from src.UI.login_gui import LoginUi
from src.UI.window_manager import window_list
from src.timekeeper import timekeeper

EXIT_SUCCESS = 0

def cleanup():
    """Cleanup resources from application"""
    # Stop the timekeeper
    timekeeper.running = False
    timekeeper.timer_thread.join()

def start(arguments):
    """Main entry point for application"""
    argument_parser = ArgumentParser(
        prog='python main.py',
        description='Starts the train control system application'
    )
    argument_parser.add_argument('--testing', '-t', action='store_true',
                                 help='Launch the application for testing')
    args = argument_parser.parse_args(arguments)

    # Create the application
    app = QtWidgets.QApplication(sys.argv)

    # Start the timekeeper
    timekeeper.start_time()

    # If we are testing, pass control back to test script
    if args.testing:
        return app

    window_list.append(LoginUi())
    try:
        app.exec_()
    finally:
        cleanup()

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(start(sys.argv[1:]))
