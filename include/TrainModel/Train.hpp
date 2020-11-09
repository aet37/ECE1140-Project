/**
 * Created by Kenneth Meier
 * Train implementation class
 */
#ifndef TRAIN_MODEL_TRAIN_HPP
#define TRAIN_MODEL_TRAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

namespace TrainModel
{

class Train
{
public:
    /**
     * @brief Creates a new Train object
     */
    Train();

    ///////////////////////////////////////////////////////////////
    // SETTERS AND GETTERS
    ///////////////////////////////////////////////////////////////

    // COMMAND SPEED
    /**
     * @brief Setter function for Command Speed
     * @param commandSpeed
     */
    void SetCommandSpeed(int commandSpeed) { m_commandSpeed = commandSpeed; };

    /**
     * @brief gets CommandSpeed
     * @return returns CommandSpeed
     */
    int GetCommandSpeed() const { return m_commandSpeed; }

    // CURRENT SPEED
    /**
     * @brief Setter function for currentSpeed
     * @param currentSpeed
     */
    void SetCurrentSpeed(int currentSpeed) { m_currentSpeed = currentSpeed; };

    /**
     * @brief gets currentSpeed
     * @return returns currentSpeed
     */
    int GetCurrentSpeed() const { return m_currentSpeed; }

    // POSITION
    /**
     * @brief Setter function for position
     * @param position
     */
    void SetPosition(int position) { m_position = position; };

    /**
     * @brief gets position
     * @return returns position
     */
    int GetPosition() const { return m_position; }

    // AUTHORITY
    /**
     * @brief Setter function for authority
     * @param authority
     */
    void SetAuthority(int authority) { m_authority = authority; };

    /**
     * @brief gets authority
     * @return returns authority
     */
    int GetAuthority() const { return m_authority; }

    // TEMP CONTROL
    /**
     * @brief Setter function for tempControl
     * @param tempControl
     */
    void SetTempControl(int tempControl) { m_tempControl = tempControl; };

    /**
     * @brief gets tempControl
     * @return returns tempControl
     */
    int GetTempControl() const { return m_tempControl; }

    // EMERGENCY PASSENGER BRAKE
    /**
     * @brief Setter function for emergencyPassengeBrake
     * @param emergencyPassengeBrake
     */
    void SetEmergencyPassengeBrake(bool emergencyPassengeBrake) { m_emergencyPassengeBrake = emergencyPassengeBrake; };

    /**
     * @brief gets emergencyPassengeBrake
     * @return returns emergencyPassengeBrake
     */
    bool GetEmergencyPassengeBrake() const { return m_emergencyPassengeBrake; }

    // SERVICE BRAKE
    /**
     * @brief Setter function for serviceBrake
     * @param serviceBrake
     */
    void SetServiceBrake(bool serviceBrake) { m_serviceBrake = serviceBrake; };

    /**
     * @brief gets serviceBrake
     * @return returns serviceBrake
     */
    bool GetServiceBrake() const { return m_serviceBrake; }

    // BRAKE COMMAND
    // ASK COLLIN ABOUT THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // What is the diff between service brake and brake command?
    /**
     * @brief Setter function for brakeCommand
     * @param brakeCommand
     */
    void SetBrakeCommand(bool brakeCommand) { m_brakeCommand = brakeCommand; };

    /**
     * @brief gets brakeCommand
     * @return returns brakeCommand
     */
    bool GetBrakeCommand() const { return m_brakeCommand; }

    // HEAD LIGHTS
    /**
     * @brief Setter function for headLights
     * @param headLights
     */
    void SetHeadLights(bool headLights) { m_headLights = headLights; };

    /**
     * @brief gets headLights
     * @return returns headLights
     */
    bool GetHeadLights() const { return m_headLights; }

    // CABIN LIGHTS
    /**
     * @brief Setter function for cabinLights
     * @param cabinLights
     */
    void SetCabinLights(bool cabinLights) { m_cabinLights = cabinLights; };

    /**
     * @brief gets cabinLights
     * @return returns cabinLights
     */
    bool GetCabinLights() const { return m_cabinLights; }

    // ADVERTISEMENTS
    /**
     * @brief Setter function for advertisements
     * @param advertisements
     */
    void SetAdvertisements(bool advertisements) { m_advertisements = advertisements; };

    /**
     * @brief gets advertisements
     * @return returns advertisements
     */
    bool GetAdvertisements() const { return m_advertisements; }

    // ANNOUNCEMENTS
    /**
     * @brief Setter function for announcements
     * @param announcements
     */
    void SetAnnouncements(bool announcements) { m_announcements = announcements; };

    /**
     * @brief gets announcements
     * @return returns announcements
     */
    bool GetAnnouncements() const { return m_announcements; }

    // DOORS
    /**
     * @brief Setter function for doors
     * @param doors
     */
    void SetDoors(bool doors) { m_doors = doors; };

    /**
     * @brief gets doors
     * @return returns doors
     */
    bool GetDoors() const { return m_doors; }

    // CURRENT BLOCK
    /**
     * @brief Setter function for currentBlock
     * @param currentBlock
     */
    void SetCurrentBlock(int currentBlock) { m_currentBlock = currentBlock; };

    /**
     * @brief gets currentBlock
     * @return returns currentBlock
     */
    int GetCurrentBlock() const { return m_currentBlock; }

    // TRAIN LENGTH
    /**
     * @brief Setter function for trainLength
     * @param trainLength
     */
    void SetTrainLength(int trainLength) { m_trainLength = trainLength; };

    /**
     * @brief gets trainLength
     * @return returns trainLength
     */
    int GetTrainLength() const { return m_trainLength; }

    // TRAIN WIDTH
    /**
     * @brief Setter function for trainWidth
     * @param trainLength
     */
    void SetTrainWidth(int trainWidth) { m_trainWidth = trainWidth; };

    /**
     * @brief gets trainWidth
     * @return returns trainWidth
     */
    int GetTrainWidth() const { return m_trainWidth; }

    // TRAIN HEIGHT
    /**
     * @brief Setter function for trainHeight
     * @param trainHeight
     */
    void SetTrainHeight(int trainHeight) { m_trainHeight = trainHeight; };

    /**
     * @brief gets trainHeight
     * @return returns trainHeight
     */
    int GetTrainHeight() const { return m_trainHeight; }

    // TRAIN MASS
    /**
     * @brief Setter function for trainMass
     * @param trainMass
     */
    void SetTrainMass(int trainMass) { m_trainMass = trainMass; };

    /**
     * @brief gets trainMass
     * @return returns trainMass
     */
    int GetTrainMass() const { return m_trainMass; }

    // TRAIN CREW COUNT
    /**
     * @brief Setter function for trainCrewCount
     * @param trainCrewCount
     */
    void SetTrainCrewCount(int trainCrewCount) { m_trainCrewCount = trainCrewCount; };

    /**
     * @brief gets trainCrewCount
     * @return returns trainCrewCount
     */
    int GetTrainCrewCount() const { return m_trainCrewCount; }

    // TRAIN PASS COUNT
    /**
     * @brief Setter function for trainPassCount
     * @param trainPassCount
     */
    void SetTrainPassCount(int trainPassCount) { m_trainPassCount = trainPassCount; };

    /**
     * @brief gets trainPassCount
     * @return returns trainPassCount
     */
    int GetTrainPassCount() const { return m_trainPassCount; }

    // SIGNAL PICKUP FAILURE
    /**
     * @brief Setter function for signalPickupFailure
     * @param signalPickupFailure
     */
    void SetSignalPickupFailure(bool signalPickupFailure) { m_signalPickupFailure = signalPickupFailure; };

    /**
     * @brief gets signalPickupFailure
     * @return returns signalPickupFailure
     */
    bool GetSignalPickupFailure() const { return m_signalPickupFailure; }

    // ENGINE FAILURE
    /**
     * @brief Setter function for engineFailure
     * @param engineFailure
     */
    void SetEngineFailure(bool engineFailure) { m_engineFailure = engineFailure; };

    /**
     * @brief gets engineFailure
     * @return returns engineFailure
     */
    bool GetEngineFailure() const { return m_engineFailure; }

    // BRAKE FAILURE
    /**
     * @brief Setter function for brakeFailure
     * @param brakeFailure
     */
    void SetBrakeFailure(bool brakeFailure) { m_brakeFailure = brakeFailure; };

    /**
     * @brief gets brakeFailure
     * @return returns brakeFailure
     */
    bool GetBrakeFailure() const { return m_brakeFailure; }

    // MODE
    /**
     * @brief Setter function for mode
     * @param mode
     */
    void SetMode(bool mode) { m_mode = mode; };

    /**
     * @brief gets mode
     * @return returns mode
     */
    bool GetMode() const { return m_mode; }

protected:
private:
    // INTEGERS (Vital)
    int m_commandSpeed;
    int m_currentSpeed; // THIS IS CALCULATED
    int m_position; // THIS IS CALCULATED
    int m_authority;
    int m_currentBlock;
    // INTEGERS (Nonvital)
    int m_tempControl;
    // BOOLEANS (Vital)
    bool m_emergencyPassengeBrake;
    bool m_serviceBrake;
    bool m_brakeCommand;
    // BOOLEANS (Nonvital)
    bool m_headLights;
    bool m_cabinLights;
    bool m_advertisements;
    bool m_announcements;
    bool m_doors;

    // Parameter Inputs
    int m_trainLength;
    int m_trainWidth;
    int m_trainHeight;
    int m_trainMass;
    int m_trainCrewCount;
    int m_trainPassCount;

    // Failure cases
    bool m_signalPickupFailure;
    bool m_engineFailure;
    bool m_brakeFailure;

    // MISC.
    bool m_mode;  // Auto or Manual
};

} // namespace TrainModel

#endif // TRAIN_MODEL_TRAIN_HPP