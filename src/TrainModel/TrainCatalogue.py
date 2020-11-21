# Created by Kenneth Meier
# Train implementation class

# SYSTEM INCLUDES
import sys
sys.path.append(".")

# Python PROJECT INCLUDES
from src.TrainModel.Train import Train
from src.signals import signals
class TrainCatalogue:
    # Call "m_trainlist.count()" for amount of trains
    # Call "m_trainlist.append()" to add a train
    # Call "m_trainlist[#]" to load a specific train
    def __init__ (self):
        self.m_trainList = []

        # Receive dispatch train signal
        signals.train_model_dispatch_train.connect(self.train_model_dispatch_train)
        # Receive lights signal
        signals.train_model_gui_receive_lights.connect(self.train_model_receive_lights)
        # Receive doors signal
        signals.train_model_gui_receive_doors.connect(self.train_model_receive_doors)
        # Receive announcements signal
        signals.train_model_gui_receive_announce_stations.connect(self.train_model_gui_receive_announce_stations)
        # Receive advertisements signal
        signals.train_model_gui_receive_ads.connect(self.train_model_gui_receive_ads)
        # Receive temperature signal
        signals.train_model_gui_receive_sean_paul.connect(self.train_model_gui_receive_sean_paul)
        # Receive mode signal
        signals.train_model_gui_receive_mode.connect(self.train_model_gui_receive_mode)
        # Receive service brake signal
        signals.train_model_gui_receive_service_brake.connect(self.train_model_gui_receive_service_brake)

    # print(sys.path)

    ###############################################################
    # Signal Methods
    ###############################################################

    # @brief Gets the train's route
    def train_model_dispatch_train(self, trainId, destinationBlock, commandSpeed, authority, currentLine):
        # Create new train object
        newTrain = Train(trainId)

        # Edit the train with the dispatched values
        newTrain.m_destinationBlock = destinationBlock
        newTrain.m_commandSpeed = commandSpeed
        newTrain.m_authority = authority
        newTrain.m_currentLine = currentLine

        # Add the train to the array
        self.m_trainList.append(newTrain)

        # Let Collin know a train has been dispatched
        signals.swtrain_dispatch_train.emit(commandSpeed, 0, authority)

        # Tell the gui something has changed
        signals.train_model_something_has_been_changed.emit()
        
    # @brief Toggles the train lights
    def train_model_receive_lights(self, trainId, cabinLights):
        self.m_trainList[trainId].m_cabinLights = cabinLights
        signals.train_model_something_has_been_changed.emit()

    # @brief Toggles the train doors
    def train_model_receive_doors(self, trainId, doors):
        self.m_trainList[trainId].m_doors = doors
        signals.train_model_something_has_been_changed.emit()

    # @brief Toggles the announcements
    def train_model_gui_receive_announce_stations(self, trainId, announcements):
        self.m_trainList[trainId].m_announcements = announcements
        signals.train_model_something_has_been_changed.emit()

    # @brief Toggles the advertisements
    def train_model_gui_receive_ads(self, trainId, ads):
        self.m_trainList[trainId].m_advertisements = ads
        signals.train_model_something_has_been_changed.emit()

    # @brief Sets the temperature
    def train_model_gui_receive_sean_paul(self, trainId, temperature):
        self.m_trainList[trainId].m_tempControl = temperature
        signals.train_model_something_has_been_changed.emit()

    # @brief Toggles the train mode
    def train_model_gui_receive_mode(self, trainId, mode):
        self.m_trainList[trainId].m_mode = mode
        signals.train_model_something_has_been_changed.emit()

    def train_model_gui_receive_service_brake(self, trainId, service_brake):
        self.m_trainList[trainId].m_serviceBrake = service_brake
        signals.train_model_something_has_been_changed.emit()
        pass

train_catalogue = TrainCatalogue()