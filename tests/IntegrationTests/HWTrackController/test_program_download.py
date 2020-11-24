"""Test for downloading a program to the arduino"""

import sys
from time import sleep

sys.path.insert(1, '../../..')
from src.HWTrackController.hw_track_controller_connector import Code

def test_blank_controller(connector):
    """Ensure we can start then immediately end a download"""
    # Start download
    connector.send_message("{} Blank Program".format(Code.START_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # End download
    connector.send_message("{}".format(Code.END_DOWNLOAD.value))
    assert connector.get_response() == b'0'

def test_program_download(connector):
    """Downloads a simple program to the arduino"""
    # Start download
    connector.send_message("{} Blank Program".format(Code.START_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # Create a tag
    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "MyTag",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "output2",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    # Create a periodic task
    connector.send_message("{} {}".format(Code.CREATE_TASK.value,
                                             "PERIOD 2000 MainTask"))
    assert connector.get_response() == b'0'

    # Create the main routine
    connector.send_message("{} {}".format(Code.CREATE_ROUTINE.value,
                                             "Main"))
    assert connector.get_response() == b'0'

    # Create a rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add three instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIC MyTag"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIC output2"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTU output2"))
    assert connector.get_response() == b'0'

    # Create a new rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add three instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIO MyTag"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIO output2"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTL output2"))
    assert connector.get_response() == b'0'

    # Create a new rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add two instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIO output2"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTU MyTag"))
    assert connector.get_response() == b'0'

    # Create a new rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add two instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIC output2"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTL MyTag"))
    assert connector.get_response() == b'0'

    # End download
    connector.send_message("{}".format(Code.END_DOWNLOAD.value))
    assert connector.get_response() == b'0'

def test_lcd_downloading(connector):
    """Verify that the lcd display shows Downloading... during a download"""
    # Start download
    connector.send_message("{}".format(Code.START_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # Given some time for verification
    sleep(10)

def test_ote_instruction(connector):
    """Downloads a simple program with ote instructions to the arduino"""
    # Start download
    connector.send_message("{}".format(Code.START_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # Create a tag
    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "MyTag",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "output2",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    # Create a periodic task
    connector.send_message("{} {}".format(Code.CREATE_TASK.value,
                                             "PERIOD 2000 MainTask"))
    assert connector.get_response() == b'0'

    # Create the main routine
    connector.send_message("{} {}".format(Code.CREATE_ROUTINE.value,
                                             "Main"))
    assert connector.get_response() == b'0'

    # Create a new rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add three instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIO MyTag"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIO output2"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTE output2"))
    assert connector.get_response() == b'0'

    # Create a new rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add two instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIC output2"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTE MyTag"))
    assert connector.get_response() == b'0'

    # End download
    connector.send_message("{}".format(Code.END_DOWNLOAD.value))
    assert connector.get_response() == b'0'

def test_get_all_tag_values(connector):
    """Downloads a program with just tags and verifies the GET_ALL_TAG_VALUES command"""
    # Start download
    connector.send_message("{}".format(Code.START_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # Create tags
    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "heater",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "switch",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "b0O",
                                             "TRUE"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {} {}".format(Code.CREATE_TAG.value,
                                             "output2",
                                             "FALSE"))
    assert connector.get_response() == b'0'

    # End download
    connector.send_message("{}".format(Code.END_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # Test the GET_ALL_TAG_VALUES command
    connector.send_message("{}".format(Code.GET_ALL_TAG_VALUES.value))
    assert connector.get_response() == b"heater 0 switch 0 b0O 1 output2 0"


if __name__ == "__main__":
    raise Exception("Run using pytest")
