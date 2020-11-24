"""Common tests across modules"""

import sys
import pytest

sys.path.append(".")
from main import start, cleanup
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system

@pytest.fixture(scope='function')
def start_app():
    """Starts the application with the testing flag"""
    start(['--testing'])
    yield
    cleanup()

def test_toggle_lights(start_app):
    """Testing toggling the lights"""

    signals.train_model_dispatch_train.emit(0, 0, 0, 0, 0)

    signals.swtrain_gui_toggle_cabin_lights.emit(0)

    assert control_system.p_controllers[0].lights
    assert train_catalogue.m_trainList[0].m_cabinLights
