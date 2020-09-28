"""Script to build and upload to an arduino"""

from argparse import ArgumentParser
import os
import subprocess
import sys

import logging
logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
ARDUINO_CLI = 'arduino-cli.exe'

def build_sketch(path_to_sketch):
    """Builds the provided sketch using the Arduino CLI.

    :param str path_to_sketch: Path to sketch to build

    """
    logger.info("Building sketch {}".format(path_to_sketch))

    build_proc = subprocess.Popen([ARDUINO_CLI, 'compile', '--fqbn', 'arduino:avr:mega', path_to_sketch])
    build_proc.wait()

    if (build_proc.returncode != 0):
        raise BaseException("Build was not successful")

    logger.info("Built successfully")

def upload_sketch(path_to_sketch):
    """Uploads the provided sketch using the Arduino CLI.

    :param str path_to_sketch: Path to sketch to upload

    """
    logger.info("Uploading sketch {}".format(path_to_sketch))

    board_check = subprocess.check_output([ARDUINO_CLI, 'board', 'list'])
    if board_check == b'No boards found.\n':
        raise BaseException("Board must be connected to upload")

    upload_proc = subprocess.Popen([ARDUINO_CLI, 'upload', '-p', 'COM3', '--fqbn', 'arduino:avr:mega', path_to_sketch])
    upload_proc.wait()

    if (upload_proc.returncode != 0):
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
    argument_parser.add_argument('--upload', '-u', action='store_true',
                                 help='Just uploads the sketch')
    args = argument_parser.parse_args()

    if not os.path.isfile(ARDUINO_CLI):
        raise ValueError("Arduino CLI must be installed")

    if not os.path.isdir(args.sketch):
        raise ValueError("Sketch must be a file")

    logging.basicConfig(level=logging.INFO)

    if not args.upload:
        build_sketch(args.sketch)

    if not args.build:
        upload_sketch(args.sketch)

    logger.info("Script Complete: SUCCESS")
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
