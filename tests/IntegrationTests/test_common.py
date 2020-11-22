"""Common tests across modules"""

import sys
from time import sleep
import pytest

sys.path.insert(1, '.')
from main import start, cleanup
from src.UI.login_gui import LoginUi
from src.UI.window_manager import window_list

@pytest.fixture(scope='function')
def start_app():
    app = start(['--testing'])
    yield app
    cleanup()

def test_login(start_app):
    """Test logging into everyone's page"""
    login = LoginUi()

    usernames = ['ctc', 'swtrack', 'trackmodel', 'trainmodel', 'swtrain', 'timekeeper']
    password = 'jerry'

    for username in usernames:
        login.username_in.setText(username)
        login.password_in.setText(password)
        login.login_parse()
        start_app.processEvents()
        sleep(0.5)

    assert len(window_list) == len(usernames)

    sleep(3)

