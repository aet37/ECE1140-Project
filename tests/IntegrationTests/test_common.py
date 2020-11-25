"""Common tests across modules"""

import sys

sys.path.append(".")
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system
from src.CTC.TrainSystem import ctc
from src.common_def import Line
from src.TrackModel.TrackModelDef import SignalHandler

def test_dispatch_train(start_app):
    """Tests dispatching a train and ensures all modules react accordingly"""

    # Upload track
    fileInfoGreen = ['resources/Green Line.xlsx', 'All Files (*)']
    SignalHandler.readInData(fileInfoGreen)

    fileInfoRed = ['resources/Red Line.xlsx', 'All Files (*)']
    SignalHandler.readInData(fileInfoRed)

    # Send dispatch signal
    ctc.DispatchTrain(38, Line.LINE_GREEN)

    # Assert train is made in CTC
    assert ctc.trains_arr[0].train_id == 1

    # Assert train is made in swtrain, trainmodel
    assert len(train_catalogue.m_trainList) == 1
    assert len(control_system.p_controllers) == 1

    # Assert received authority and command speed
    assert train_catalogue.m_trainList[0].m_commandSpeed == 24.85484
    assert train_catalogue.m_trainList[0].m_authority

    assert control_system.p_controllers[0].command_speed == 40.0
    assert control_system.p_controllers[0].authority
