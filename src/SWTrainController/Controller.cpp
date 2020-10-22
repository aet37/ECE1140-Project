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
    speed_limit = 0;
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
}

/** 
 * @brief initializes data coming from train model
 * @param com_sp = command speed
 * @param curr_sp = current speed
 * @param sp_lim = speed limit
 * @param auth = authority
 */
Controller::Controller(int com_sp, int curr_sp, int sp_lim, int auth)
{
    command_speed = com_sp;
    current_speed = curr_sp;
    speed_limit = sp_lim;
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
}

///////////////////////////////////////////////////////////////
// SETTERS AND GETTERS
///////////////////////////////////////////////////////////////

/**
 * @brief Setter function for Kp
 * @param KP = kp
 */
void Controller::setKp(int KP)
{
    kp = KP;
}

/**
 * @brief Setter function for Ki
 * @param KI = ki
 */
void Controller::setKi(int KI)
{
    ki = KI;
}

/**
 * @brief Setter function for command speed
 * @param com_sp == command_speed
 */
void Controller::setCommandSpeed(int com_sp)
{
    command_speed = com_sp;
}

/**
 * @brief Setter function for current speed
 * @param curr_sp == current_speed
 */
void Controller::setCurrentSpeed(int curr_sp)
{
    current_speed = curr_sp;
}

/**
 * @brief Setter function for speed limit
 * @param sp_lim == speed limit
 */
void Controller::setSpeedLimit(int sp_lim)
{
    speed_limit = sp_lim;
}

/**
 * @brief Setter function for authority
 * @param auth == auth
 */
void Controller::setAuthority(int auth)
{
    authority = auth;
}

/**
 * @brief Getter function for command speed
 * @return command_speed
 */
int Controller::getCommandSpeed()
{
    return command_speed;
}

/**
 * @brief Getter function for current speed
 * @return current_speed
 */
int Controller::getCurrentSpeed()
{
    return current_speed;
}

/**
 * @brief Getter function for speed limit
 * @return speed limit
 */
int Controller::getSpeedLimit()
{
    return speed_limit;
}

/**
 * @brief Getter function for authority
 * @return authority
 */
int Controller::getAuthority()
{
    return authority;
}

/**
 * @brief Getter function for power command
 */
int Controller::getPowerCommand()
{
    return power_command;
}

///////////////////////////////////////////////////////////////
// VITAL OPERATIONS
///////////////////////////////////////////////////////////////
/**
 * @brief default calculate power function for testing purposes
 */
void Controller::calculatePower()
{
    power_command = (kp + ki) * command_speed;
}
/**
 * @brief calculates power command that will be sent to train model
 */
void Controller::calculatePower(int T)
{
    // Find Verror
    int Verror = command_speed - current_speed;

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
 * @param input_speed = speed train driver inputs if train is in manual mode
 */
void Controller::regulateSpeed(int input_speed)
{
    //
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
 * @brief allows operator to switch between manual and automatic mode
 * @param override = string code entered by operator to initiate manual override
 */
void Controller::toggleMode(std::string override)
{

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
void setCabinTemp(int temp)
{
    NVO.temperature = temp;
}

/**
 * @brief gets temperature of train cabin
 * @return returns temperature of cabin
 */
int getCabinTemp()
{
    return NVO.temperature;
}