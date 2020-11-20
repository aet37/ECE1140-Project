# Created by Kenneth Meier
# Train implementation class

# SYSTEM INCLUDES
import sys
sys.path.append(".")

# Python PROJECT INCLUDES
from Train.py import Train
from signals import signals
class TrainCatalogue:
    # Receive dispatch train signal
    signals.TRAIN_MODEL_DISPATCH_TRAIN.connect(train_model_dispatch_train)
    # Receive lights signal
    signals.TRAIN_MODEL_GUI_RECEIVE_LIGHTS.connect(train_model_gui_receive_lights)

    # Call "m_trainlist.count()" for amount of trains
    # Call "m_trainlist.append()" to add a train
    # Call "m_trainlist[#]" to load a specific train
    def __init__ (self):
        self.m_trainList = []
    # print(sys.path)

    ###############################################################
    # Signal Methods
    ###############################################################

    # @brief Gets the train's route
    def train_model_dispatch_train(self, trainId, destinationBlock, commandSpeed, authority, currentLine):
        # Create new train object
        newTrain = Train.__init__(trainId)

        # Edit the train with the dispatched values
        newTrain.m_destinationBlock = destinationBlock
        newTrain.m_commandSpeed = commandSpeed
        newTrain.m_authority = authority
        newTrain.m_currentLine = currentLine

        # Add the train to the array
        self.m_trainList.append(newTrain)
        return self.m_route

    # @brief Toggles the train lights
    def train_model_dispatch_train(self, trainId, destinationBlock, commandSpeed, authority, currentLine):
        newTrain = Train.__init__()
        self.m_trainList.append()
        return self.m_route
