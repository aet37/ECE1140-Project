//
// Created by Collin Hough on 10.07.20
// Control System implementation file
//

#include "ControlSystem.h"

Controller* ControlSystem::createNewController(float com_sp, float curr_sp, bool auth)
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