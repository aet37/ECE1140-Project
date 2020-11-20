"""Test for downloading a program to the arduino"""

import sys
from time import sleep

sys.path.insert(1, '../../../src')
from HWTrackController.hw_track_controller_connector import Code

def test_emit_program(connector):
    """Downloads a program that uses an EMIT instruction"""
    # Start download
    connector.send_message("{} Emit Program".format(Code.START_DOWNLOAD.value))
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

    # Add instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "XIC MyTag"))
    assert connector.get_response() == b'0'

    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "EMIT MyTagEvent"))
    assert connector.get_response() == b'0'

    # Create an event driven task
    connector.send_message("{} {}".format(Code.CREATE_TASK.value,
                                          "EVENT MyTagEvent EventDrivenTask"))
    assert connector.get_response() == b'0'

    # Create the main routine
    connector.send_message("{} {}".format(Code.CREATE_ROUTINE.value,
                                             "Main"))
    assert connector.get_response() == b'0'

    # Create a rung
    connector.send_message("{}".format(Code.CREATE_RUNG.value))
    assert connector.get_response() == b'0'

    # Add instructions
    connector.send_message("{} {}".format(Code.CREATE_INSTRUCTION.value,
                                          "OTL output2"))
    assert connector.get_response() == b'0'

    # End download
    connector.send_message("{}".format(Code.END_DOWNLOAD.value))
    assert connector.get_response() == b'0'

    # Wait a few seconds before setting the tag
    sleep(5)

    # Set MyTag
    connector.send_message("{} {}".format(Code.SET_TAG_VALUE.value,
                                          "MyTag 1"))
    assert connector.get_response() == b'0'


if __name__ == "__main__":
    raise Exception("Run using pytest")
