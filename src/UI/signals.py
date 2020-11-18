from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSignal

class SignalsObject(QObject):
    # CTC Signals #

    # SWTrackController Signals #

    # HWTrainController Signals #

    # Track Model Signals #

    # Train Model Signals #

    # SWTrainController Signals #
    SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS = pyqtSignal(int) # TrainID
    SWTRAIN_DISPATCH_TRAIN = pyqtSignal(float, float, bool) # command speed, current speed, authority
    SWTRAIN_UPDATE_CURRENT_SPEED = pyqtSignal(int, float) # TrainID, current speed
    SWTRAIN_UPDATE_COMMAND_SPEED = pyqtSignal(int, float) # TrainID, command speed 
    SWTRAIN_UPDATE_AUTHORITY = pyqtSignal(int, bool) # TrainID, authority
    SWTRAIN_CAUSE_FAILURE = pyqtSignal(bool, bool, bool) # Failures
    SWTRAIN_PULL_PASSENGER_EBRAKE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_PULL_EBRAKE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_SET_SETPOINT_SPEED = pyqtSignal(int, float) # TrainID, Setpoint Speed
    SWTRAIN_GUI_PRESS_SERVICE_BRAKE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_TOGGLE_DAMN_DOORS = pyqtSignal(int) # TrainID 
    SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_SET_SEAN_PAUL = pyqtSignal(int, float) # TrainID, temperature
    SWTRAIN_GUI_ANNOUNCE_STATIONS = pyqtSignal(int) # TrainID 
    SWTRAIN_GUI_DISPLAY_ADS = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_RESOLVE_FAILURE = pyqtSignal(int) # TrainID
    SWTRAIN_GUI_SET_KP_KI = pyqtSignal(int, float, float) # TrainID, setKp, setKi
    SWTRAIN_GUI_SWITCH_MODE = pyqtSignal(int, str) # TrainID, override code
    SWTRAIN_TIME_TRIGGER = pyqtSignal() 

    # HWTrainController Signals #


Signals = SignalsObject()