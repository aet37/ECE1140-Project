"""Tests for interactions between the train model and sw train controller"""

import sys
sys.path.insert(1, '.')
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system
from src.timekeeper import timekeeper
import time
from src.TrackModel.TrackModelDef import red_route_blocks, green_route_blocks


def test_toggle_lights(start_app):
    """Testing toggling the lights"""

    signals.train_model_dispatch_train.emit(0, 38, 15, 0, 0, green_route_blocks)

    signals.swtrain_gui_toggle_cabin_lights.emit(0)

    assert control_system.p_controllers[0].lights
    assert train_catalogue.m_trainList[0].m_cabinLights

def test_power_loop(start_app):
    """Testing the power loop"""
    # Dispatch a train from the train model
    signals.train_model_dispatch_train.emit(0, 38, 15, 0, 0, green_route_blocks)

    # Set kp and ki
    signals.swtrain_gui_set_kp_ki.emit(0, 200, 200)

    # Set time to ten times wall clock speed
    timekeeper.time_factor = 0.05

    # Wait until speed is reached
    while(True):
        time.sleep(0.05)
        signals.swtrain_time_trigger.emit()
        if round(control_system.p_controllers[0].current_speed, 2) == 9.32:
            break
        assert round(control_system.p_controllers[0].current_speed, 2) < 9.32
        assert round(train_catalogue.m_trainList[0].m_currentSpeed, 2) < 9.32

        if timekeeper.current_time_min > 10:
            assert False

    # Check to make sure speed is maintained
    minutes = timekeeper.current_time_min
    while(True):
        assert round(control_system.p_controllers[0].current_speed, 2) == 9.32
        assert round(train_catalogue.m_trainList[0].m_currentSpeed, 2) == 9.32
        if (timekeeper.current_time_min == (minutes + 5)):
            break
