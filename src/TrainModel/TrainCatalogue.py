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


train_catalogue = TrainCatalogue()