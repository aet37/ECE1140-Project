"""Common fixtures for tests"""

import sys
import pytest

sys.path.insert(1, '../../..')
from src.HWTrackController.hw_track_controller_connector import HWTrackCtrlConnector

# pylint: disable=redefined-outer-name
@pytest.fixture(scope='session')
def connector():
    """Creates a connector to communicate to the arduino"""
    return HWTrackCtrlConnector()
