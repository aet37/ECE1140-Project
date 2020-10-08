//
// Created by Collin Hough on 10.7.20
// Defines controller sytem that encompasses all active train controllers
//
#ifndef CONTROLSYSTEM_H
#define CONTROLSYSTEM_H

#include "SWTrainDef.h"
#include "Controller.h"
#include <vector>

class ControlSystem
{
    private:
        // Controllers
        std::vector<Controller*> p_controllers;

    public:

        /**
         * @param train_id = Train ID
         * 
         * @return Pointer to Controller struct
         */ 
        Controller* createNewController(int com_sp, int curr_sp, int sp_lim, int auth);

};
#endif