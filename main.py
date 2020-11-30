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
from src.TrackModel.TrackModelDef import SignalHandler
from src.HWTrackController.hw_track_controller_connector import HWTrackCtrlConnector
from src.SWTrackController.track_system import track_system
from src.SWTrackController.Compiler.lexer import Lexer
from src.SWTrackController.Compiler.emitter import Emitter
from src.SWTrackController.Compiler.parse import Parser
from src.logger import get_logger

logger = get_logger(__name__)

EXIT_SUCCESS = 0

def auto_download_plc_programs():
    """Downloads plc programs to track controllers"""
    logger.critical("Auto downloading plc programs")
    for i, track_controller in enumerate(track_system.green_track_controllers):

        source_code = ''
        for line in open('resources/Track Controller PLC Programs/Green{}.txt'.format(i)):
            source_code += line

        output_file = 'CompiledOutput.txt'
        lex = Lexer(source_code)
        emitter = Emitter(output_file)
        par = Parser(lex, emitter)
        par.program("Green{}".format(i))

        track_controller.download_program(output_file)

def auto_upload_tracks():
    """Uploads the red and green track"""
    logger.critical("Auto uploading tracks")
    # Upload track
    file_info_green = ['resources/Green Line.xlsx', 'All Files (*)']
    SignalHandler.readInData(file_info_green)

    file_info_red = ['resources/Red Line.xlsx', 'All Files (*)']
    SignalHandler.readInData(file_info_red)

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
    logger.critical("Cleaning up resources")
    # Stop the timekeeper
    timekeeper.stop_time()

    # Stop any hardware connectors
    HWTrackCtrlConnector.run_timer = False

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
                                 help='Opens one additional gui')
    argument_parser.add_argument('--auto_upload', '-u', action='store_true',
                                 help='Auto uploads the red and green track')
    argument_parser.add_argument('--auto_download', '-d', action='store_true',
                                 help='Auto downloads plc programs to track controllers')
    args = argument_parser.parse_args(arguments)

    # Start the timekeeper
    timekeeper.start_time()

    # Upload the tracks automatically if selected
    if args.auto_upload:
        auto_upload_tracks()

    # Download plc programs to controllers if selected
    if args.auto_download:
        auto_download_plc_programs()

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
