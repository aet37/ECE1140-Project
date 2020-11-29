"""Tests for interactions between the train model and sw train controller"""

import polling
import pytest
import sys
import math
sys.path.insert(1, '.')
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system
from src.timekeeper import timekeeper
from src.TrackModel.TrackModelDef import green_route_blocks
from src.common_def import Line


def test_toggle_lights():
    """Testing toggling the lights"""

    signals.train_model_dispatch_train.emit(0, 38, 15, 0, Line.LINE_GREEN, green_route_blocks)

    signals.swtrain_gui_toggle_cabin_lights.emit(0)

    assert control_system.p_controllers[0].lights
    assert train_catalogue.m_trainList[0].m_cabinLights

def test_power_loop(upload_tracks, start_timekeeper):
    """Testing the power loop"""
    # Disconnect unimportant signals
    signals.trackmodel_update_occupancy.disconnect()

    # Dispatch a train from the train model
    signals.train_model_dispatch_train.emit(0, 38, 15, 0, Line.LINE_GREEN, green_route_blocks)

    # Set kp and ki
    signals.swtrain_gui_set_kp_ki.emit(0, 200, 200)

    # Set time to ten times wall clock speed
    timekeeper.time_factor = 0.05

    polling.poll(raise_speed, step=0.05, timeout=60)

    with pytest.raises(polling.PollingException):
        polling.poll(maintain_speed, step=0.1, timeout=10)

def raise_speed():
    """Emits the time trigger signal and ensures speed doesn't break threshold"""
    signals.swtrain_time_trigger.emit()

    assert math.isclose(control_system.p_controllers[0].current_speed, 9.32, rel_tol=0.5)
    assert math.isclose(train_catalogue.m_trainList[0].m_currentSpeed, 9.32, rel_tol=0.5)

    return round(control_system.p_controllers[0].current_speed, 2) == 9.32

def maintain_speed():
    """Emits the time trigger signal and ensures speed still doesn't break threshold"""
    signals.swtrain_time_trigger.emit()

    assert math.isclose(control_system.p_controllers[0].current_speed, 9.32, rel_tol=0.5)
    assert math.isclose(train_catalogue.m_trainList[0].m_currentSpeed, 9.32, rel_tol=0.5)
    