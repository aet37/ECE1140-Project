//
// Created by Collin Hough on 10.07.20
// Control System implementation file
//

#include "ControlSystem.h"

Controller* ControlSystem::createNewController(int com_sp, int curr_sp, int sp_lim, int auth)
{
    // Create new controller
    Controller* p_temp = new Controller(com_sp, curr_sp, sp_lim, auth);

    // Add controller to vector of controllers (Keep everything singleton)
    p_controllers.push_back(p_temp);

    // Return instance of controller
    return p_temp;
}