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
                // uint32_t com_sp = req.ParseData<uint32_t>(1);
                // uint32_t curr_sp = req.ParseData<uint32_t>(2);
                // uint32_t auth = req.ParseData<uint32_t>(3);
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
                // Common::Request newRequest(Common::RequestCode:: , lightStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController doors: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_ANNOUNCE_STATIONS:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Controller tempController = TrainControllers.getControllerInstance(TrainID);
                // uint32_t announcementStatus = tempController.announceStations();
                // std::string announcementStatusString = std::to_string(announcementStatus);
                // Common::Request newRequest(Common::RequestCode:: , lightStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController announcements: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_DISPLAY_ADS:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Controller tempController = TrainControllers.getControllerInstance(TrainID);
                // uint32_t adsStatus = tempController.toggleAds();
                // std::string adsStatusString = std::to_string(adsStatus);
                // Common::Request newRequest(Common::RequestCode:: , lightStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController advertisements: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_SET_SEAN_PAUL:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                uint32_t temperature = req.ParseData<uint32_t>(1);
                // Controller tempController = TrainControllers.getControllerInstance(TrainID);
                // tempController.setCabinTemp(temperature);
                // uint32_t tempStatus = tempController.getCabinTemp(temperature);
                // std::string tempStatusString = std::to_string(tempStatus);
                // Common::Request newRequest(Common::RequestCode:: , tempStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController current temperature: %d", temperature);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_SWITCH_MODE:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Controller tempController = TrainControllers.getControllerInstance(TrainID);
                // uint32_t modeStatus = tempController.toggleMode(override);
                // std::string modeStatusString = std::to_string(modeStatus);
                // Common::Request newRequest(Common::RequestCode:: , modeStatusString)
                // TrainModel::serviceQueue.Push(newRequest)
                LOG_SW_TRAIN_CONTROLLER("SWTrainController mode: %d", trainID);
                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }
    }
}

} // namespace SWTrainController
