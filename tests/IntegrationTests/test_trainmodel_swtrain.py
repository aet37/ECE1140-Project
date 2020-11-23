"""Tests for interactions between the train model and sw train controller"""

import sys

sys.path.insert(1, '.')
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system

def test_toggle_lights(start_app):
    """Testing toggling the lights"""

    signals.train_model_dispatch_train.emit(0, 0, 0, 0, 0)

    signals.swtrain_gui_toggle_cabin_lights.emit(0)

    assert control_system.p_controllers[0].lights
    assert train_catalogue.m_trainList[0].m_cabinLights