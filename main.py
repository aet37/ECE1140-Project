"""Main file to run"""

from argparse import ArgumentParser
import sys
from PyQt5 import QtWidgets

from src.UI.login_gui import LoginUi
from src.UI.timekeeper_gui import TimekeeperUi
from src.UI.CTC.ctc_gui import CTCUi
from src.UI.SWTrackController.swtrack_gui import SWTrackControllerUi
from src.UI.TrackModel.trackmodel_gui import TrackModelUi
from src.UI.TrainModel.trainmodel_gui import TrainModelUi
from src.UI.SWTrainController.TrainController import SWTrainUi
from src.UI.window_manager import window_list
from src.timekeeper import timekeeper

EXIT_SUCCESS = 0

def open_other_modules(args):
    """Opens additional windows based on the arguments"""
    if args.open_all:
        window_list.append(CTCUi())
        window_list.append(SWTrackControllerUi())
        window_list.append(TrackModelUi())
        window_list.append(TrainModelUi())
        window_list.append(SWTrainUi())
        window_list.append(TimekeeperUi())
    else:
        if args.open == 1:
            window_list.append(CTCUi())
        elif args.open == 2:
            window_list.append(SWTrackControllerUi())
        elif args.open == 3:
            window_list.append(TrackModelUi())
        elif args.open == 4:
            window_list.append(TrainModelUi())
        elif args.open == 5:
            window_list.append(SWTrainUi())
        elif args.open == 6:
            window_list.append(TimekeeperUi())

def cleanup():
    """Cleanup resources from application"""
    # Stop the timekeeper
    timekeeper.running = False
    timekeeper.resume_time()
    timekeeper.timer_thread.join()

def start(arguments):
    """Main entry point for application"""
    argument_parser = ArgumentParser(
        prog='python main.py',
        description='Starts the train control system application'
    )
    argument_parser.add_argument('--testing', '-t', action='store_true',
                                 help='Launch the application for testing')
    argument_parser.add_argument('--open_all', '-a', action='store_true',
                                 help='Opens every modules gui')
    argument_parser.add_argument('--open', '-o', type=int, nargs='?', default=0,
                                 help='Launch the application for testing')
    args = argument_parser.parse_args(arguments)

    # Start the timekeeper
    timekeeper.start_time()

    # If we are testing, pass control back to test script
    if args.testing:
        return EXIT_SUCCESS

    # Create the application
    app = QtWidgets.QApplication(sys.argv)

    window_list.append(LoginUi())
    open_other_modules(args)
    try:
        app.exec_()
    finally:
        cleanup()

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(start(sys.argv[1:]))
