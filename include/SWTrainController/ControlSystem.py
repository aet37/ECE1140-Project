#
# Created by Collin Hough on 10.7.20
# Defines controller sytem that encompasses all active train controllers
#
#ifndef CONTROLSYSTEM_H
#define CONTROLSYSTEM_H

#include "SWTrainDef.h"
#include "Controller.h"
#include <vector>
from include.SWTrainController.Controller import Controller
from UI.signals import Signals

class ControlSystem:
    def __init__ (self):
        # Controllers
        self.p_controllers = []

        # Receive dispatch train signal
        Signals.SWTRAIN_DISPATCH_TRAIN.connect(self.SWTRAIN_DISPATCH_TRAIN)
        # Receive lights signal
        Signals.SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS.connect(self.SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS)


    # @param train_id = Train ID
    # @return Pointer to Controller struct
    def createNewController(self, com_sp, curr_sp, auth):
        # Create new controller
        p_temp = Controller(com_sp, curr_sp, auth)

        # Add controller to vector of controllers (Keep everything singleton)
        p_controllers.append(p_temp)

        # Return instance of controller
        return p_temp

    # @param id = train_id
    # @brief Returns individual Controller from vector
    def getControllerInstance(self, id):
        return self.p_controllers[id]

    # @return Returns amount of controllers
    def getAmountofControllers(self):
        return len(self.p_controllers)

    ### SIGNAL DEFINITION ###
    def SWTRAIN_DISPATCH_TRAIN(self, com_sp, curr_sp, auth):
        self.createNewController(com_sp, curr_sp, auth)
        Signals.HWTRAIN_DISPATCH_TRAIN.emit(com_sp, curr_sp, auth)

    def SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS(self, trainID):
        self.p_controllers[trainID].toggleLights()
        Signals.TRAIN_MODEL_GUI_RECEIVE_LIGHTS.emit(trainID)

control_system = ControlSystem()
#endif