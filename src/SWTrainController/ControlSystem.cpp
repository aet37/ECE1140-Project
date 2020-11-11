//
// Created by Collin Hough on 10.07.20
// Control System implementation file
//

#include "ControlSystem.h"

/**
 * @param com_sp = command speed
 * @param curr_sp = current speed
 * @param auth = authority
 * @brief constructor to initialize a new controller
 */
ControlSystem::ControlSystem(int com_sp, int curr_sp, bool auth)
{
    // Create new controller
    Controller* p_temp = new Controller(com_sp, curr_sp, auth);

    // Add controller to vector of controllers (Keep everything singleton)
    p_controllers.push_back(p_temp);
}

Controller* ControlSystem::createNewController(int com_sp, int curr_sp, bool auth)
{
    // Create new controller
    Controller* p_temp = new Controller(com_sp, curr_sp, auth);

    // Add controller to vector of controllers (Keep everything singleton)
    p_controllers.push_back(p_temp);

    // Return instance of controller
    return p_temp;
}

/**
 * @param id = train_id
 * @brief Returns individual Controller from vector
 */
Controller* ControlSystem::getControllerInstance(int id)
{
    return p_controllers[id];
}

/**
 * @return Returns amount of controllers
 */
int ControlSystem::getAmountofControllers()
{
    return p_controllers.size();
}