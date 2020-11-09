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
        default:
            LOG_SW_TRAIN_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace SWTrainController
