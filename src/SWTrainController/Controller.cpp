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
 * @brief calculates power command that will be sent to train model
 */
void Controller::calculatePower()
{
    power_command = (kp + ki) * current_speed;
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
void Controller::toggleDoors()
{
    NVO.doors = !NVO.doors;
}

/**
 * @brief turn lights on/off
 */
void Controller::toggleLights()
{
    NVO.doors = !NVO.doors;
}

/**
 * @brief turn announcements on/off
 */
void Controller::announceStations()
{
    NVO.announcements = !NVO.announcements;
}

/**
 * @brief turn advertisements on/off
 */
void Controller::toggleAds()
{
    NVO.advertisements = !NVO.advertisements;
}

/**
 * @brief turn air-conditioning on/off
 */
void Controller::toggleAirConditioning()
{
    NVO.airConditioning = !NVO.airConditioning;
}