/**
 * @file RequestManager.cpp
 *
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrainControllerRequestManager.hpp" // Header for class
#include "SWTrainControllerMain.hpp"
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros
#include "ControlSystem.h"

namespace SWTrainController
{

void SWTrainControllerRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::SWTRAIN_DISPATCH_TRAIN:
        {
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_TOGGLE_DAMN_DOORS:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_ANNOUNCE_STATIONS:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_DISPLAY_ADS:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_SET_SEAN_PAUL:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_SWITCH_MODE:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_SET_SETPOINT_SPEED:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_PRESS_SERVICE_BRAKE:
        {
            // Add the request to the queue
            SWTrainController::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_GATHER_DATA:
        {
            Controller* pController = ControlSystem::getInstance().getControllerInstance(rRequest.ParseData<uint32_t>(0)-1);

            rResponse.AppendData(std::to_string(pController->getDoors()));            // 0
            rResponse.AppendData(std::to_string(pController->getLights()));           // 1
            rResponse.AppendData(std::to_string(pController->getAnnounceStations())); // 2
            rResponse.AppendData(std::to_string(pController->getAds()));              // 3
            rResponse.AppendData(std::to_string(pController->getCurrentSpeed()));     // 4
            rResponse.AppendData(std::to_string(pController->getCommandSpeed()));     // 5
            rResponse.AppendData(std::to_string(pController->getSetpointSpeed()));    // 6
            rResponse.AppendData(std::to_string(pController->getServiceBrake()));     // 7
            rResponse.AppendData(std::to_string(pController->getMode()));             // 8

            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SWTRAIN_GUI_UPDATE_DROP_DOWN:
        {
            uint32_t numberOfControllers = ControlSystem::getInstance().getAmountofControllers();
            rResponse.AppendData(std::to_string(numberOfControllers));
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        default:
            LOG_SW_TRAIN_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace SWTrainController
