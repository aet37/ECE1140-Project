"""
    Author: Collin Hough

    Date: 10.7.20
"""

from src.SWTrainController.Controller import Controller
from src.signals import signals

class ControlSystem:
    """ Defines controller sytem that encompasses all active train controllers """

    def __init__ (self):
        """ Initializes set of controllers """
        # Controllers
        self.p_controllers = []

        # Receive dispatch train signal
        signals.swtrain_dispatch_train.connect(self.swtrain_dispatch_train)
        # Receive lights signal
        signals.swtrain_gui_toggle_cabin_lights.connect(self.swtrain_gui_toggle_cabin_lights)

    def create_new_controller(self, com_sp, curr_sp, auth):
        """ Method to create new controller instance """
        # Create new controller
        p_temp = Controller(com_sp, curr_sp, auth)

        # Add controller to vector of controllers (Keep everything singleton)
        self.p_controllers.append(p_temp)

        # Return instance of controller
        return p_temp

    def get_controller_instance(self, train_id):
        """ Returns instance of controller from set """
        return self.p_controllers[train_id]

    def get_amount_of_controllers(self):
        """ Returns amount of controllers in system """
        return len(self.p_controllers)

    ### SIGNAL DEFINITIONS ###
    def swtrain_dispatch_train(self, com_sp, curr_sp, auth):
        """ Handler for swtrain_dispatch_train signal """
        self.create_new_controller(com_sp, curr_sp, auth)
        signals.hwtrain_dispatch_train.emit(com_sp, curr_sp, auth)

    def swtrain_gui_toggle_cabin_lights(self, train_id):
        """ Handler for swtrain_gui_toggle_lights signal """
        self.p_controllers[train_id].toggleLights()
        signals.train_model_gui_receive_lights.emit(train_id)

control_system = ControlSystem()
