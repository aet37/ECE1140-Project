# Created by Kenneth Meier
# Train implementation class

# SYSTEM INCLUDES
import sys
sys.path.append(".")

# Python PROJECT INCLUDES
from src.TrainModel.Train import Train
from src.TrainModel.Block import Block
from src.TrainModel.BlockCatalogue import block_catalogue_red, block_catalogue_green
from src.signals import signals
from src.logger import get_logger
from src.common_def import *

logger = get_logger(__name__)
class TrainCatalogue:

    
    # Call "m_trainlist.count()" for amount of trains
    # Call "m_trainlist.append()" to add a train
    # Call "m_trainlist[#]" to load a specific train
    def __init__ (self):
        self.m_trainList = []
        self.m_blockList = []

        # Acceleration Limit: 0.5 m/s^2     Deceleration Limit(service brake): 1.2 m/s^2    Deceleration Limit(emergency brake): 2.73 m/s^2
        self.MAX_FORCE = 18551.9333
        self.GRAVITY = 9.8
        self.FRICTION_COEFFICIENT = 0.01
        self.ACCELERATION_LIMIT = 0.5
        self.DECELERATION_LIMIT_SERVICE = -1.2
        self.DECELERATION_LIMIT_EMERGENCY = -2.73
        self.VELOCITY_LIMIT = 19.4444

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
        # Receive Power Loop signal
        signals.train_model_receive_power.connect(self.train_model_receive_power)
        # Receive Blocks
        signals.train_model_receive_block.connect(self.train_model_receive_block)

    # print(sys.path)

    ###############################################################
    # Signal Methods
    ###############################################################

    # @brief Gets the train's route
    def train_model_dispatch_train(self, trainId, destinationBlock, commandSpeed, authority, currentLine, route):
        logger.debug("Received train_model_dispatch_train")
        # Create new train object
        newTrain = Train(trainId)

        # Edit the train with the dispatched values
        newTrain.m_destinationBlock = destinationBlock
        newTrain.m_commandSpeed = commandSpeed * Converters.KmHr_to_MPH
        newTrain.m_authority = authority
        newTrain.m_currentLine = currentLine
        newTrain.m_route = route
        logger.debug("route[0] = %f", route[len(route)-1])

        # Add the train to the array
        self.m_trainList.append(newTrain)

        # Let Collin know a train has been dispatched
        signals.swtrain_dispatch_train.emit(commandSpeed, 0, authority)

        # Tell the gui something has changed
        signals.train_model_dropdown_has_been_changed.emit()

    # @brief Receives block information
    def train_model_receive_block(self, track_id, block_id, elevation, slope, sizeOfBlock, speedLimit, travelDirection):
        newBlock = Block(block_id)
        # Parse stuff from Evan (trackId, blockId, elevation, grade, length, speedLimit, travelDirection)

        newBlock.m_elevation = elevation
        newBlock.m_slope = slope
        newBlock.m_sizeOfBlock = sizeOfBlock
        newBlock.m_speedLimit = speedLimit
        newBlock.m_travelDirection = travelDirection

        # Add the block to the catalogue
        if (track_id == 0):
            block_catalogue_green.m_blockList.append(newBlock)
            logger.debug("Received a green block. There are now " + str(len(block_catalogue_green.m_blockList)))
        else:
            block_catalogue_red.m_blockList.append(newBlock)
            logger.debug("Received a red block. There are now " + str(len(block_catalogue_red.m_blockList)))

    # @brief Toggles the train lights
    def train_model_receive_lights(self, trainId, cabinLights):
        self.m_trainList[trainId].m_cabinLights = cabinLights
        signals.train_model_something_has_been_changed.emit()

    # @brief Receives authority
    def train_model_update_authority(self, trainId, newAuthority):
        self.m_trainList[trainId].m_authority = newAuthority
        signals.train_model_something_has_been_changed.emit()
        signals.swtrain_update_authority.emit(trainId, newAuthority)

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

        if (currentTrack == Line.LINE_GREEN):
            currentBlockSize = block_catalogue_green.m_blockList[currentBlock].m_sizeOfBlock
            speedLimitBlock = block_catalogue_green.m_blockList[currentBlock].m_speedLimit
        else:
            currentBlockSize = block_catalogue_red.m_blockList[currentBlock].m_sizeOfBlock
            speedLimitBlock = block_catalogue_red.m_blockList[currentBlock].m_speedLimit
        # currentBlockSize = 10000 # meters
        # speedLimitBlock = 70 # Km/hr
        speedLimitBlock = speedLimitBlock * Converters.KmHr_to_mps

        # LOG_TRAIN_MODEL("currentBlockSize = %f", currentBlockSize);

        commandSpeed = self.m_trainList[trainId].m_commandSpeed
        commandSpeed = commandSpeed * Converters.KmHr_to_mps # m/s
        currentSpeed = self.m_trainList[trainId].m_currentSpeed # m/s
        currentSpeed = currentSpeed * Converters.MPH_to_mps
        previousPosition = self.m_trainList[trainId].m_position
        trainMass = self.m_trainList[trainId].m_trainMass
        trainMass = trainMass * Converters.Tons_to_kg # kg
        serviceBrake = self.m_trainList[trainId].m_serviceBrake
        emergencyBrake = self.m_trainList[trainId].m_emergencyPassengeBrake
        samplePeriod = 1/5 # ASK COLLIN FOR SAMPLE PERIOD
        
        logger.debug("powerStatus = %f", powerStatus)

        # FORCE
        try:
            forceCalc = (powerStatus/currentSpeed)
            forceCalc -= self.FRICTION_COEFFICIENT * (trainMass) * self.GRAVITY
        except ZeroDivisionError:
            if(not serviceBrake):
                forceCalc = self.FRICTION_COEFFICIENT * (trainMass) * self.GRAVITY + 1000
                forceCalc -= self.FRICTION_COEFFICIENT * (trainMass) * self.GRAVITY
            else:
                forceCalc = 0.0

        logger.debug("forceCalc = %f", forceCalc)

        # ACCELERATION
        accelerationCalc = (forceCalc/trainMass) # Acceleration Limit: 0.5 m/s^2     Deceleration Limit(service brake): 1.2 m/s^2    Deceleration Limit(emergency brake): 2.73 m/s^2
        logger.debug("accelerationCalc = %f", accelerationCalc)
        if (accelerationCalc > self.ACCELERATION_LIMIT and not serviceBrake and not emergencyBrake):
            # If all brakes are OFF and accelerationCalc is above the limit
            accelerationCalc = self.ACCELERATION_LIMIT
        elif (accelerationCalc < self.DECELERATION_LIMIT_SERVICE and serviceBrake and not emergencyBrake):
            # If the service brake is ON and accelerationCalc is below the limit
            accelerationCalc = self.DECELERATION_LIMIT_SERVICE
        elif (accelerationCalc < self.DECELERATION_LIMIT_EMERGENCY and not serviceBrake and emergencyBrake):
            # If the emergency brake is ON and accelerationCalc is below the limit
            accelerationCalc = self.DECELERATION_LIMIT_EMERGENCY

        # VELOCITY
        velocityCalc = currentSpeed + (accelerationCalc/samplePeriod) # Velocity Limit: 19.4444 m/s
        logger.debug("velocityCalc in MPH = %f", velocityCalc * Converters.mps_to_MPH)
        if(velocityCalc >= self.VELOCITY_LIMIT):
            # If the velocity is GREATER than max train speed
            velocityCalc = self.VELOCITY_LIMIT # m/s
        if(velocityCalc >= speedLimitBlock):
            # If the velocity is GREATER than the block's speed limit
            velocityCalc = speedLimitBlock
            logger.debug("speedLimitBlock = %f", speedLimitBlock)
        if(velocityCalc <= 0):
            # If the velocity is LESS than 0
            velocityCalc = 0

        currentPosition = 0
        positionCalc = 0

        # if(currentBlock == self.m_trainList[trainId].m_destinationBlock):
        # # if(currentBlock == self.m_trainList[trainId].m_destinationBlock):
        #     # Set all the parameters in the train object
        #     self.m_trainList[trainId].m_power = powerStatus
        #     self.m_trainList[trainId].m_currentSpeed = 0 # For display stopping purposes

        #     # Send to Collin
        #     signals.swtrain_update_current_speed.emit(trainId, 0)

        #     # LOG_TRAIN_MODEL("Train powerStatus = %d, Train ID = %d", powerStatus, trainId);
        # else:
            # POSITION
        positionCalc = (velocityCalc/samplePeriod)
        currentPosition = previousPosition + positionCalc
            # currentPosition = previousPosition + 50 Hardcoded moving for test
        if(currentPosition > currentBlockSize):
            # Move to the next block!
            currentPosition = currentPosition - currentBlockSize # Catch overflow into next block
            self.m_trainList[trainId].m_position = currentPosition # Update position
            self.m_trainList[trainId].m_route.pop(0) # Remove the block train is on to move to nect block

            # LOG_TRAIN_MODEL("Current block is now %d", tempTrain->GetCurrentBlock())

            # Send block exited to Evan (trainid, trackid, blockId, trainOrNot
            # Send to Evan
            if (currentTrack == Line.LINE_GREEN):
                logger.debug("currentTrack = {}".format(currentTrack))
                signals.trackmodel_update_occupancy.emit(trainId, Line.LINE_GREEN, currentBlock, False)
                logger.debug("FIRST currentPosition = %f", currentPosition)
                logger.debug("FIRST currentBlock = %f", currentBlock)
            else:
                signals.trackmodel_update_occupancy.emit(trainId, Line.LINE_RED, currentBlock, False)

            # Send block entered to Evan (trainid, trackid, blockId, trainOrNot
            # Send to Evan
            if (currentTrack == Line.LINE_GREEN):
                signals.trackmodel_update_occupancy.emit(trainId, Line.LINE_GREEN, self.m_trainList[trainId].m_route[0], True)
                logger.debug("SECOND currentPosition = %f", currentPosition)
                logger.debug("SECOND self.m_trainList[trainId].m_route[0] = %f", self.m_trainList[trainId].m_route[0])
            else:
                signals.trackmodel_update_occupancy.emit(trainId, Line.LINE_RED, self.m_trainList[trainId].m_route[0], True)
        else:
            # LOG_TRAIN_MODEL("Staying in the same block: currentPosition = %f, blockSize = %f", currentPosition, currentBlockSize)
            # Still in the same block
            self.m_trainList[trainId].m_position = currentPosition

        # Set all the parameters in the train object
        
        self.m_trainList[trainId].m_power = powerStatus
        self.m_trainList[trainId].m_currentSpeed = velocityCalc * Converters.mps_to_MPH

        # Send to Collin
        signals.swtrain_update_current_speed.emit(trainId, velocityCalc * Converters.mps_to_MPH)
        # if((accelerationCalc/samplePeriod) > 0): # Check for an actual change
        signals.train_model_something_has_been_changed.emit()

        # LOG_TRAIN_MODEL("Train powerStatus = %d, Train ID = %d", powerStatus, trainId)

train_catalogue = TrainCatalogue()