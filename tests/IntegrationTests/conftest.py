"""Common fixtures across tests"""

import sys
import pytest

sys.path.insert(1, '.')
from main import cleanup, auto_upload_tracks
from src.timekeeper import timekeeper

@pytest.fixture(scope='module')
def start_timekeeper():
    """Starts the application with the testing flag"""
    timekeeper.start_time()
    yield
    cleanup()

@pytest.fixture(scope='module')
def upload_tracks():
    """Fixture to upload the track"""
    auto_upload_tracks()
