"""Common fixtures across tests"""

import sys
import pytest

sys.path.insert(1, '.')
from main import start, cleanup

@pytest.fixture(scope='module')
def start_app():
    """Starts the application with the testing flag"""
    start(['--testing', '--auto_upload'])
    yield
    cleanup()
