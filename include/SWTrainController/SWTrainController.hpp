//
// Created by Collin Hough on 10.08.20
// Namespace for SW Train Controller
//

#ifndef SWTRAINCONTROLLER_HPP
#define SWTRAINCONTROLLER_HPP

namespace Controller
{
    int power_command;
    /*int authority;
    int current_speed;
    int command_speed;
    int speed_limit;
    int train_id;*/

    /**
     * @brief set function to calculate power
     * @param com_sp = command speed
     */
    void setPowerCommand(int com_sp)
    {
        power_command = 2 * cs;
    }

    int getPowerCommand()
    {
        return power_command;
    }


}

#endif