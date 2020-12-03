#ifndef HWTRAINCOMMUNICATIONS
#define HWTRAINCOMMUNICATIONS


namespace HWTrainCommunications
{

enum class RequestCode
{
    INVALID = 1,
    CHECK = 2,

    HWTRAIN_PULL_EBRAKE = 224, // Used by the HW Train Ctrl to pull the train's ebrake
    HWTRAIN_SET_SETPOINT_SPEED = 225, // Used by the HW Train Ctrl to set a train's setpoint speed
    HWTRAIN_PRESS_SERVICE_BRAKE = 226, // Used by the HW Train Ctrl to update use a train's service brake
    HWTRAIN_TOGGLE_DAMN_DOORS = 227, // Used by the HW Train Ctrl to toggle a train's door
    HWTRAIN_TOGGLE_CABIN_LIGHTS = 228, // Used by the HW Train Ctrl to toggle a train's lights
    HWTRAIN_SET_TEMPERATURE = 229, // Used by the HW Train Ctrl to play temperature by sean paul
    HWTRAIN_ANNOUNCE_STATIONS = 230, // Used by the HW Train Ctrl to announce stations
    HWTRAIN_DISPLAY_ADS = 231, // Used by the HW Train Ctrl to display a train's advertisements
    HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST = 232, // Used by the connector script to check if any requests exist for the hardware
    HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE = 233, // Used by the connector script to forward the hardware's response to the server
    HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE = 234, // Used by HW Train Ctrl to get response from the hardware
    HWTRAIN_DISPATCH_TRAIN = 235, // Used by HWTrainController to signify a train has been dispatched
    HWTRAIN_UPDATE_CURRENT_SPEED = 236, // Used by the train model to update a train's current speed
    HWTRAIN_UPDATE_COMMAND_SPEED = 237, // Used by the train model to update a train's command speed
    HWTRAIN_UPDATE_AUTHORITY = 238, // Used by the train model to update a train's authority
    HWTRAIN_SIGNAL_FAILURE = 239, // Used by the train model to cause a train's failure
    HWTRAIN_PULL_PASSENGER_EBRAKE = 240, // Used by the train model to pull a train's passenger e-brake
    HWTRAIN_GUI_GATHER_DATA = 241, // Used by the gui to update the user interface
    HWTRAIN_ENGINE_FAILURE = 242, // Used by the gui to resolve a train failure
    HWTRAIN_GUI_SET_KP = 243, // Set Kp
    HWTRAIN_GUI_GET_MODE = 244, // Displays the mode
    HWTRAIN_GUI_DISPLAY_POWER = 245, // Displays power
    HWTRAIN_GUI_SET_KI = 246, // Set Ki
    HWTRAIN_BRAKE_FAILURE = 247,
    HWTRAIN_GET_DATA = 248,
    HWTRAIN_SEND_SIGFAIL_DATA = 249,
    HWTRAIN_SEND_ENGFAIL_DATA = 250,
    HWTRAIN_SEND_BRAKEFAIL_DATA = 251,
    HWTRAIN_SEND_POWER_DATA = 252,
    HWTRAIN_SEND_SETSP_DATA = 253,
};

enum class ResponseCode
{
    SUCCESS = 0,
    ERROR = 1,
};

int Menu(int);
void CommsTask();

}

#endif 