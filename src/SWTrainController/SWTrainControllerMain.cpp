/**
 * @file SWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrainControllerMain.hpp" // Header for functions
#include "HWTrainControllerMain.hpp"
#include "TrainModelMain.hpp"
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"
#include "ControlSystem.h"

namespace SWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_SW_TRAIN_CONTROLLER("Thread starting...");
    // ControlSystem TrainControllers;
    while(true)
    {
        Common::Request req = serviceQueue.Pop();
        switch(req.GetRequestCode())
        {  
            case Common::RequestCode::SWTRAIN_DISPATCH_TRAIN:
            {
                uint32_t theInt = req.ParseData<uint32_t>(0);
                std::string theIntString = std::to_string(theInt);
                Common::Request newRequest(Common::RequestCode::HWTRAIN_DISPATCH_TRAIN, theIntString);
                // TrainControllers.createNewController(com_sp, curr_sp, auth);
                HWTrainController::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController dispatch train %s", theIntString.c_str());
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Controller tempController = TrainControllers.getControllerInstance(TrainID);
                // uint32_t lightStatus = tempController.toggleLights();
                // std::string lightStatusString = std::to_string(lightStatus);
                // Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_SET_THE_DAMN_LIGHTS, lightStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController lights: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_TOGGLE_DAMN_DOORS:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Controller tempController = TrainControllers.getControllerInstance(TrainID);
                // uint32_t doorStatus = tempController.toggleDoors();
                // std::string doorStatusString = std::to_string(doorStatus);
                // Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_SET_THE_DAMN_LIGHTS, lightStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController doors: %d", trainID);
                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }
    }
}

} // namespace SWTrainController
