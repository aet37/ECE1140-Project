/**
 * @file DebugRequestManager.cpp
 *
 * @brief Implementation of DebugRequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "DebugRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros
#include "CTCMain.hpp"
#include "HWTrackControllerMain.hpp"
#include "SWTrackControllerMain.hpp"
#include "TrackModelMain.hpp"
#include "TrainModelMain.hpp"
#include "HWTrainControllerMain.hpp"
#include "SWTrainControllerMain.hpp"

namespace Debug
{

void DebugRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    // Get the actual request information from the debug request
    Common::RequestCode reqCode = rRequest.ParseData<Common::RequestCode>(0);
    
    // We need to separate out the request code from the data now
    std::string containedRequest = rRequest.GetData();
    std::string data = containedRequest.substr(containedRequest.find_first_of(' ') + 1);

    // Create the new request
    Common::Request newRequest(reqCode, data);

    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::DEBUG_TO_CTC:
            CTC::serviceQueue.Push(newRequest);
            break;
        case Common::RequestCode::DEBUG_TO_HWTRACKCTRL:
            HWTrackController::serviceQueue.Push(newRequest);
            break;
        case Common::RequestCode::DEBUG_TO_SWTRACKCTRL:
            SWTrackController::serviceQueue.Push(newRequest);
            break;
        case Common::RequestCode::DEBUG_TO_TRACK_MODEL:
            TrackModel::serviceQueue.Push(newRequest);
            break;
        case Common::RequestCode::DEBUG_TO_TRAIN_MODEL:
            TrainModel::serviceQueue.Push(newRequest);
            break;
        case Common::RequestCode::DEBUG_TO_HWTRAINCTRL:
            HWTrainController::serviceQueue.Push(newRequest);
            break;
        case Common::RequestCode::DEBUG_TO_SWTRAINCTRL:
            SWTrainController::serviceQueue.Push(newRequest);
            break;
        default:
            LOG_DEBUG("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace Debug
