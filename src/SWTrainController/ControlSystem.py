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
        # Receive mode signal
        signals.swtrain_gui_switch_mode.connect(self.swtrain_gui_switch_mode)
        # Receive setpoint speed signal
        signals.swtrain_gui_set_setpoint_speed.connect(self.swtrain_gui_set_setpoint_speed)
        # Receive service brake signal
        signals.swtrain_gui_press_service_brake.connect(self.swtrain_gui_press_service_brake)

        ## RECEIVE NONVITAL SIGNALS ##
        # Receive lights signal
        signals.swtrain_gui_toggle_cabin_lights.connect(self.swtrain_gui_toggle_cabin_lights)
        # Receive doors signal
        signals.swtrain_gui_toggle_damn_doors.connect(self.swtrain_gui_toggle_damn_doors)
        # Receive announcements signal
        signals.swtrain_gui_announce_stations.connect(self.swtrain_gui_announce_stations)
        # Receive advertisements signal
        signals.swtrain_gui_display_ads.connect(self.swtrain_gui_display_ads)
        # Receive temperature signal
        signals.swtrain_gui_set_sean_paul.connect(self.swtrain_gui_set_sean_paul)

    def create_new_controller(self, com_sp, curr_sp, auth):
        """ Method to create new controller instance """
        # Create new controller
        p_temp = Controller(com_sp, curr_sp, auth)

        # Add controller to vector of controllers (Keep everything singleton)
        self.p_controllers.append(p_temp)

    def get_amount_of_controllers(self):
        """ Returns amount of controllers in system """
        return len(self.p_controllers)

    ### SIGNAL DEFINITIONS ###
    def swtrain_dispatch_train(self, com_sp, curr_sp, auth):
        """ Handler for swtrain_dispatch_train signal """
        control_system.create_new_controller(com_sp, curr_sp, auth)
        # If first train, dispatch to HWTrainController
        if self.get_amount_of_controllers == 0:
            signals.hwtrain_dispatch_train.emit(com_sp, curr_sp, auth)

    def swtrain_gui_switch_mode(self, train_id, override):
        """ Handler for swtrain_gui_switch_mode """
        self.p_controllers[train_id].toggle_mode(override)
        signals.train_model_gui_receive_mode.emit(train_id, self.p_controllers[train_id].mode)

    def swtrain_gui_set_setpoint_speed(self, train_id, setpoint_speed):
        """ Handler for swtrain_gui_set_setpoint_speed """
        self.p_controllers[train_id].setpoint_speed = setpoint_speed

    def swtrain_gui_press_service_brake(self, train_id):
        """ Handler for swtrain_gui_press_service_brake """
        self.p_controllers[train_id].toggle_service_brake()
        signals.train_model_gui_receive_service_brake.emit(train_id, self.p_controllers[train_id].service_brake)

    def swtrain_gui_set_kp_ki(self, train_id, Kp, Ki):
        """ Handler for swtrain_gui_set_kp_ki """
        self.p_controllers[train_id].kp = Kp
        self.p_controllers[train_id].ki = Ki

    ## NonVital Signal Definitions ##
    def swtrain_gui_toggle_cabin_lights(self, train_id):
        """ Handler for swtrain_gui_toggle_lights signal """
        self.p_controllers[train_id].toggle_lights()
        signals.train_model_gui_receive_lights.emit(train_id, self.p_controllers[train_id].lights)

    def swtrain_gui_toggle_damn_doors(self, train_id):
        """ Handler for swtrain_gui_toggle_damn_doors """
        print("hello collin")
        self.p_controllers[train_id].toggle_doors()
        signals.train_model_gui_receive_doors.emit(train_id, self.p_controllers[train_id].doors)

    def swtrain_gui_announce_stations(self, train_id):
        """ Handler for swtrain_gui_announce_stations """
        self.p_controllers[train_id].toggle_announcements()
        signals.train_model_gui_receive_announce_stations.emit(train_id, self.p_controllers[train_id].announcements)

    def swtrain_gui_display_ads(self, train_id):
        """ Handler for swtrain_gui_display_ads """
        self.p_controllers[train_id].toggle_ads()
        signals.train_model_gui_receive_ads.emit(train_id, self.p_controllers[train_id].advertisements)

    def swtrain_gui_set_sean_paul(self, train_id, temperature):
        """ Handler for swtrain_gui_set_sean_paul """
        self.p_controllers[train_id].temperature = temperature
        signals.train_model_gui_receive_sean_paul.emit(train_id, temperature)

control_system = ControlSystem()
