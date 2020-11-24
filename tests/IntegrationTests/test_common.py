"""Common tests across modules"""

import sys

sys.path.insert(1, '.')
from src.signals import signals
from src.TrainModel.TrainCatalogue import train_catalogue
from src.SWTrainController.ControlSystem import control_system
from src.CTC.TrainSystem import ctc
from src.common_def import Line
from src.TrackModel import TrackModelDef
import pyexcel
import pyexcel_io

def test_dispatch_train(start_app):
    """Tests dispatching a train and ensures all modules react accordingly"""

    # Upload track
    dialog = QtWidgets.QFileDialog.selectFile("C:/Users/Evan/OneDrive/Documents/GitHub/ECE1140-Project/resources/Green Line.xlsx")
    fileInfo = dialog.getOpenFileName(self)
    TrackModelDef.SignalHandler.readInData(self, fileInfo)
    dialog = QtWidgets.QFileDialog.selectFile("C:/Users/Evan/OneDrive/Documents/GitHub/ECE1140-Project/resources/Red Line.xlsx")
    fileInfo = dialog.getOpenFileName(self)
    TrackModelDef.SignalHandler.readInData(self, fileInfo)
    #TrackModelDef.SignalHandler.readInData("\'C:/Users/Evan/OneDrive/Documents/GitHub/ECE1140-Project/resources/Green Line.xlsx\', \'All Files (*)\')")


    # Send dispatch signal
    signals.swtrack_dispatch_train.emit(0, 38, 25.0, 3, Line.LINE_GREEN,
                                        [0, 0, 0, 1, 1, 1, 0, 1, 0, 0])

    # Assert train is made in CTC
    assert ctc.trains_arr[0].train_id == 0

    # Assert train is made in swtrain, trainmodel
    assert len(train_catalogue.m_trainList) == 1
    assert len(control_system.p_controllers) == 1

    # Assert received authority and command speed
    assert train_catalogue.m_trainList[0].m_commandSpeed == 25.0
    assert train_catalogue.m_trainList[0].m_authority

    assert control_system.p_controllers[0].command_speed == 25.0
    assert control_system.p_controllers[0].authority
