# Created by Kenneth Meier
# Train implementation class

# SYSTEM INCLUDES
import sys
sys.path.append(".")

# Python PROJECT INCLUDES
from src.TrainModel.Train import Train
from src.TrainModel.Block import Block
from src.TrainModel.BlockCatalogue import block_catalogue
from src.signals import signals
class TrainCatalogue:
    # Call "m_trainlist.count()" for amount of trains
    # Call "m_trainlist.append()" to add a train
    # Call "m_trainlist[#]" to load a specific train
    def __init__ (self):
        self.m_trainList = []
        self.m_blockList = []

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

    def train_model_receive_power(self, trainId, powerStatus):
        currentTrack = self.m_trainList[trainId].m_currentLine
        currentBlock = self.m_trainList[trainId].m_route[0]
        # LOG_TRAIN_MODEL("currentTrack = %d", currentTrack);
        # LOG_TRAIN_MODEL("currentBlock = %d", currentBlock);
        # LOG_TRAIN_MODEL("currentBlockInfo = 0x%x", currentBlockInfo);

        # LOG_TRAIN_MODEL("Number of green line blocks = %d", BlockCatalogue::GetInstance().GetNumberOfGreenBlocks());
        # LOG_TRAIN_MODEL("Number of trains = %d", TrainCatalogue::GetInstance().GetNumberOfTrains());

        currentBlockSize = self.m_blockList[currentBlock].m_sizeOfBlock
        speedLimitBlock = self.m_blockList[currentBlock].m_speedLimit

        # LOG_TRAIN_MODEL("currentBlockSize = %f", currentBlockSize);

        commandSpeed = self.m_trainList[trainId].m_commandSpeed
        previousPosition = self.m_trainList[trainId].m_position
        trainMass = self.m_trainList[trainId].m_trainMass
        serviceBrake = self.m_trainList[trainId].m_serviceBrake
        emergencyBrake = self.m_trainList[trainId].m_emergencyPassengeBrake
        samplePeriod = 1/10 # ASK COLLIN FOR SAMPLE PERIOD
        
        # FORCE
        forceCalc = (powerStatus/commandSpeed)

        # ACCELERATION
        accelerationCalc = (forceCalc/trainMass) # Acceleration Limit: 0.5 m/s^2     Deceleration Limit(service brake): 1.2 m/s^2    Deceleration Limit(emergency brake): 2.73 m/s^2
        if (accelerationCalc > 0.5 and not serviceBrake and not emergencyBrake):
            # If all brakes are OFF and accelerationCalc is above the limit
            accelerationCalc = 0.5
        elif (accelerationCalc < -1.2 and serviceBrake and not emergencyBrake):
            # If the service brake is ON and accelerationCalc is below the limit
            accelerationCalc = -1.2
        elif (accelerationCalc < -2.73 and not serviceBrake and emergencyBrake):
            # If the emergency brake is ON and accelerationCalc is below the limit
            accelerationCalc = -2.73

        # VELOCITY
        velocityCalc = (accelerationCalc/samplePeriod); # Velocity Limit: 70km/h
        if(velocityCalc > 70):
            # If the velocity is GREATER than max train speed
            velocityCalc = 70 # km/h
        if(velocityCalc > speedLimitBlock):
            # If the velocity is GREATER than the block's speed limit
            velocityCalc = speedLimitBlock

        currentPosition = 0;
        positionCalc = 0;

        if(currentBlock == self.m_trainList[trainId].m_destinationBlock):
            # Set all the parameters in the train object
            self.m_trainList[trainId].m_power = powerStatus
            self.m_trainList[trainId].m_currentSpeed = 0 # For display stopping purposes

            # Send to Collin
            # Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED);
            # newRequest.AppendData(std::to_string(trainId));
            # newRequest.AppendData(std::to_string(0)); # For display stopping purposes
            # SWTrainController::serviceQueue.Push(newRequest);

            # LOG_TRAIN_MODEL("Train powerStatus = %d, Train ID = %d", powerStatus, trainId);
        else:
            # POSITION
            positionCalc = (velocityCalc/samplePeriod)
            currentPosition = previousPosition + positionCalc;
            # currentPosition = previousPosition + 50 Hardcoded moving for test
        if(currentPosition > currentBlockSize):
            # Move to the next block!
            currentPosition = currentPosition - currentBlockSize # Catch overflow into next block
            self.m_trainList[trainId].m_position = currentPosition # Update position
            self.m_trainList[trainId].m_route.pop(0) # Remove the block train is on to move to nect block

            # LOG_TRAIN_MODEL("Current block is now %d", tempTrain->GetCurrentBlock())

            # Send block exited to Evan (trainid, trackid, blockId, trainOrNot)
            # Common::Request newRequest1(Common::RequestCode::TRACK_MODEL_UPDATE_OCCUPANCY)
            # newRequest1.AppendData(std::to_string(trainId))
            # newRequest1.AppendData(std::to_string(currentTrack))
            # newRequest1.AppendData(std::to_string(currentBlock)) # This is now the old block
            # newRequest1.AppendData(std::to_string(0))
            # TrackModel::serviceQueue.Push(newRequest1)

            # Send block entered to Evan (trainid, trackid, blockId, trainOrNot)
            # Common::Request newRequest2(Common::RequestCode::TRACK_MODEL_UPDATE_OCCUPANCY)
            # newRequest2.AppendData(std::to_string(trainId))
            # newRequest2.AppendData(std::to_string(currentTrack))
            # newRequest2.AppendData(std::to_string(tempTrain->GetCurrentBlock()))
            # newRequest2.AppendData(std::to_string(1))
            # TrackModel::serviceQueue.Push(newRequest2)
        else:
            # LOG_TRAIN_MODEL("Staying in the same block: currentPosition = %f, blockSize = %f", currentPosition, currentBlockSize)
            # Still in the same block
            self.m_trainList[trainId].m_position = currentPosition

        # Set all the parameters in the train object
        self.m_trainList[trainId].m_power = powerStatus
        self.m_trainList[trainId].m_currentSpeed = velocityCalc

        # Send to Collin
        # Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED)
        # newRequest.AppendData(std::to_string(trainId))
        # newRequest.AppendData(std::to_string(velocityCalc))
        # SWTrainController::serviceQueue.Push(newRequest)

        # LOG_TRAIN_MODEL("Train powerStatus = %d, Train ID = %d", powerStatus, trainId)

train_catalogue = TrainCatalogue()