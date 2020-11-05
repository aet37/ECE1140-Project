"""Script to build and upload to an arduino"""

from argparse import ArgumentParser
import os
import subprocess
import sys

import logging
logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
ARDUINO_CLI = 'arduino-cli'

def run_initialization():
    """Installs required packages."""
    logger.info("Beginning initialization")

    update_proc = subprocess.Popen([ARDUINO_CLI, 'core', 'update-index'])
    update_proc.wait()

    if update_proc.returncode != 0:
        raise BaseException("Update index failed")

    install_proc = subprocess.Popen([ARDUINO_CLI, 'core', 'install', 'arduino:avr'])
    install_proc.wait()

    if install_proc.returncode != 0:
        raise BaseException("Install failed")

    install_lib_proc = subprocess.Popen([ARDUINO_CLI, 'lib', 'install', '"LiquidCrystal I2C"'])
    install_lib_proc.wait()

    if install_lib_proc.returncode != 0:
        raise BaseException("Install library failed")

    logger.info("Finished initialization successfully")

def build_sketch(path_to_sketch, debug):
    """Builds the provided sketch using the Arduino CLI.

    :param str path_to_sketch: Path to sketch to build
    :param bool debug: Whether to build with the debug flag

    """
    logger.info("Building sketch %s", path_to_sketch)

    arguments = [ARDUINO_CLI, 'compile', '--fqbn',
                 'arduino:avr:mega', path_to_sketch]

    if debug:
        arguments += ['--build-properties', 'build.extra_flags=-DDEBUGENABLE']

    build_proc = subprocess.Popen(arguments)
    build_proc.wait()

    if build_proc.returncode != 0:
        raise BaseException("Build was not successful")

    logger.info("Built successfully")

def upload_sketch(path_to_sketch):
    """Uploads the provided sketch using the Arduino CLI.

    :param str path_to_sketch: Path to sketch to upload

    """
    logger.info("Uploading sketch %s", path_to_sketch)

    board_check = subprocess.check_output([ARDUINO_CLI, 'board', 'list'])
    if board_check == b'No boards found.\n':
        raise BaseException("Board must be connected to upload")

    upload_proc = subprocess.Popen([ARDUINO_CLI, 'upload', '-p', 'COM3',
                                    '--fqbn', 'arduino:avr:mega', path_to_sketch])
    upload_proc.wait()

    if upload_proc.returncode != 0:
        raise BaseException("Upload was not successful")

    logger.info("Uploaded successfully")

def main():
    """Main entry point of script."""
    argument_parser = ArgumentParser(
        prog='python build_and_upload.py arduino_sketch',
        description='Builds and uploads a sketch to an arduino'
	)
    argument_parser.add_argument('sketch', help='Sketch to build and upload')
    argument_parser.add_argument('--build', '-b', action='store_true',
                                 help='Just builds the sketch')
    argument_parser.add_argument('--debug', '-d', action='store_true',
                                 help='Sets the DEBUGENABLE build flag')
    argument_parser.add_argument('--upload', '-u', action='store_true',
                                 help='Just uploads the sketch')
    argument_parser.add_argument('--initialize', '-i', action='store_true',
                                 help='Installs required packages before building/uploading')
    args = argument_parser.parse_args()

    if not os.path.isdir(args.sketch):
        raise ValueError("Sketch must be a file")

    logging.basicConfig(level=logging.INFO)

    if args.initialize:
        run_initialization()

    if not args.upload:
        build_sketch(args.sketch, args.debug)

    if not args.build:
        upload_sketch(args.sketch)

    logger.info("Script Complete: SUCCESS")
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
