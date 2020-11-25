"""Common fixtures for tests"""

import time
import pytest

from src.HWTrackController.hw_track_controller_connector import HWTrackCtrlConnector

# pylint: disable=redefined-outer-name
@pytest.fixture(scope='session')
def connector():
    """Creates a connector to communicate to the arduino"""
    con = HWTrackCtrlConnector()
    time.sleep(3)
    return con
