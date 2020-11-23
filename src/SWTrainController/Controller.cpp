//
// Created by Collin Hough on 10.7.20
// Controller implementation file
//

#include "Controller.h"

/**
 * @brief initialize variables
 */
Controller::Controller()
{
    // Initialize vital variables
    command_speed = 0;
    current_speed = 0;
    setpoint_speed = 0;
    power_command = 0;
    authority = 0;
    mode = 0;
    serviceBrake = 0;
    emergencyBrake = 0;
    kp = 0;
    ki = 0;
    uk = 0;
    uk1 = 0;
    ek = 0;
    ek1 = 0;
    signalPickupFailure = 0;
    engineFailure = 0;
    brakeFailure = 0; 
    NonVitalOperations();
}

/** 
 * @brief initializes data coming from train model
 * @param com_sp = command speed
 * @param curr_sp = current speed
 * @param auth = authority
 */
Controller::Controller(float com_sp, float curr_sp, bool auth)
{
    command_speed = com_sp;
    current_speed = curr_sp;
    setpoint_speed = 0;
    power_command = 0;
    authority = auth;
    mode = 0;
    serviceBrake = 0;
    emergencyBrake = 0;
    kp = 0;
    ki = 0;
    uk = 0;
    uk1 = 0;
    ek = 0;
    ek1 = 0;
    signalPickupFailure = 0;
    engineFailure = 0;
    brakeFailure = 0;
    NonVitalOperations();
}

///////////////////////////////////////////////////////////////
// SETTERS AND GETTERS
///////////////////////////////////////////////////////////////

/**
 * @brief Setter function for Kp
 * @param KP = kp
 */
void Controller::setKp(float KP)
{
    kp = KP;
}

/**
 * @brief Setter function for Ki
 * @param KI = ki
 */
void Controller::setKi(float KI)
{
    ki = KI;
}

/**
 * @brief Setter function for command speed
 * @param com_sp == command_speed
 */
void Controller::setCommandSpeed(float com_sp)
{
    command_speed = com_sp;
}

/**
 * @brief Setter function for current speed
 * @param curr_sp == current_speed
 */
void Controller::setCurrentSpeed(float curr_sp)
{
    current_speed = curr_sp;
}

/**
 * @brief Setter function for setpoint speed
 * @param setp_sp == setpoint speed
 */
void Controller::setSetpointSpeed(float setp_sp)
{
    setpoint_speed = setp_sp;
}

/**
 * @brief Setter function for authority
 * @param auth == auth
 */
void Controller::setAuthority(bool auth)
{
    authority = auth;
}

/**
 * @brief Getter function for command speed
 * @return command_speed
 */
float Controller::getCommandSpeed()
{
    return command_speed;
}

/**
 * @brief Getter function for current speed
 * @return current_speed
 */
float Controller::getCurrentSpeed()
{
    return current_speed;
}

/**
 * @brief Getter function for setpoint speed
 * @return setpoint speed
 */
float Controller::getSetpointSpeed()
{
    return setpoint_speed;
}

/**
 * @brief Getter function for authority
 * @return authority
 */
bool Controller::getAuthority()
{
    return authority;
}

/**
 * @brief Getter function for power command
 */
float Controller::getPowerCommand()
{
    return power_command;
}

/**
 * @brief Getter function for mode
 */
bool Controller::getMode()
{
    return mode;
}

/**
 * @brief Getter function for service brake
 */
bool Controller::getServiceBrake()
{
    return serviceBrake;
}

// Non-Vital Getters
/**
 * @brief open/close doors
 */
bool Controller::getDoors()
{
    return NVO.doors;
}

/**
 * @brief turn lights on/off
 */
bool Controller::getLights()
{
    return NVO.lights;
}

/**
 * @brief turn announcements on/off
 */
bool Controller::getAnnounceStations()
{
    return NVO.announcements;
}

/**
 * @brief turn advertisements on/off
 */
bool Controller::getAds()
{
    return NVO.advertisements;
}

///////////////////////////////////////////////////////////////
// VITAL OPERATIONS
///////////////////////////////////////////////////////////////
/**
 * @brief calculates power command that will be sent to train model
 */
void Controller::calculatePower()
{
    // Find Verror depending on mode
    float Verror = 0;
    if (mode == 0) // Automatic Mode
        Verror = command_speed - current_speed;
    else // Manual Mode
        Verror = setpoint_speed - current_speed;

    // Set ek as the kth sample of velocity error
    ek = Verror;

    // Determine uk as shown in slide 65 of lecture 2
    if (power_command < MAX_POWER)
    {
        // Find uk 
        uk = uk1 + (T/2) * (ek + ek1);
    }
    else
    {
        uk = uk1;
    }
    
    // Find power command
    power_command = (kp * ek) + (ki * uk);

    // Set past values of uk and ek
    uk1 = uk;
    ek1 = ek;

}

/**
 * @brief ensures train does not exceed speed limit
 * @brief if train is in automatic mode, speed is set to command speed
 * @brief if train is in manual mode, speed is set to setpoint speed
 */
void Controller::regulateSpeed()
{
    // Check mode of operation (Automatic or Manual)
        // Automatic Mode
            // C
        // Manual Mode
}

/**
 * @brief safety critical aspect to stop train immediately
 */
void Controller::activateEmergencyBrake()
{
    emergencyBrake = 1;
}

/**
 * @brief safety critical aspect to reset emergency brake
 */
void Controller::resetEmergencyBrake()
{
    emergencyBrake = 0;
}

/**
 * @brief toggle service brake on and off
 */
bool Controller::toggleServiceBrake()
{
    serviceBrake = !serviceBrake;
    return serviceBrake;
}

/**
 * @brief allows operator to switch between manual and automatic mode
 * @param override = string code entered by operator to initiate manual override
 * @return returns boolean value to signify success of operation
 */
bool Controller::toggleMode(std::string override)
{
    // Check if override code is correct
    if (override == password)
    {
        mode = !mode;
        return mode;
    }
    else
        return 0;
}

///////////////////////////////////////////////////////////////
// NON-VITAL OPERATIONS
///////////////////////////////////////////////////////////////
/**
 * @brief open/close doors
 */
bool Controller::toggleDoors()
{
    NVO.doors = !NVO.doors;
    return NVO.doors;
}

/**
 * @brief turn lights on/off
 */
bool Controller::toggleLights()
{
    NVO.lights = !NVO.lights;
    return NVO.lights;
}

/**
 * @brief turn announcements on/off
 */
bool Controller::announceStations()
{
    NVO.announcements = !NVO.announcements;
    return NVO.announcements;
}

/**
 * @brief turn advertisements on/off
 */
bool Controller::toggleAds()
{
    NVO.advertisements = !NVO.advertisements;
    return NVO.advertisements;
}

/**
 * @brief sets temperature of train cabin
 * @param temp = temperature cabin is set to
 */
void Controller::setCabinTemp(float temp)
{
    NVO.temperature = temp;
}

/**
 * @brief gets temperature of train cabin
 * @return returns temperature of cabin
 */
float Controller::getCabinTemp()
{
    return NVO.temperature;
}