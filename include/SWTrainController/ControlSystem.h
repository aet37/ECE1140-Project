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
        ControlSystem() {}
        /**
         * @param com_sp = command speed
         * @param curr_sp = current speed
         * @param auth = authority
         * @brief constructor to initialize a new controller
         */
        ControlSystem(int com_sp, int curr_sp, bool auth);

        /**
         * @param train_id = Train ID
         * 
         * @return Pointer to Controller struct
         */ 
        Controller* createNewController(int com_sp, int curr_sp, bool auth);

        /**
         * @param id = train_id
         * @brief Returns individual Controller from vector
         */
        Controller* getControllerInstance(int id);

        /**
         * @return Returns amount of controllers
         */
        int getAmountofControllers();
};
#endif