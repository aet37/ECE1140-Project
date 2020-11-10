/**
 * @file SWTrackControllerRequestManager.cpp
*/

// SYSTEM INCLUDES
#include <iostream>

// C++ PROJECT INCLUDES
#include "SWTrackControllerRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp"   // For LOG macros
#include "SWTrackControllerMain.hpp"  // For SWTrackController::serviceQueue
#include "HWTrackControllerRequestManager.hpp" // For HWTrackController::RequestManager

// Difference between swtrack and hwtrack request codes
static const uint32_t REQUEST_CODE_DIFFERENCE = 22;

namespace SWTrackController
{

void SWTrackControllerRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    // Holds the track controller number when a download starts
    static uint32_t trackControllerNumber = 0;

    switch(rRequest.GetRequestCode())
    {
        case Common::RequestCode::SWTRACK_GUI_GATHER_DATA:
        {
            trackControllerNumber = rRequest.ParseData<uint32_t>(0);
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            break;
        }
        case Common::RequestCode::SWTRACK_GUI_SET_SWITCH_POSITION:
        {
            trackControllerNumber = rRequest.ParseData<uint32_t>(0);
            if (trackControllerNumber == HW_TRACK_CONTROLLER_NUMBER)
            {
                Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "switch " + rRequest.ParseData<std::string>(1));
                HWTrackController::HWTrackControllerRequestManager reqManager;
                reqManager.HandleRequest(newReq, rResponse);
            }
            else
            {
                Common::Request newReq(Common::RequestCode::SET_TAG_VALUE, "switch " + rRequest.GetData());
                SWTrackController::serviceQueue.Push(rRequest);
                rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            }
            break;
        }
        case Common::RequestCode::START_DOWNLOAD:
        {
            trackControllerNumber = rRequest.ParseData<uint32_t>(1);
            if (trackControllerNumber == HW_TRACK_CONTROLLER_NUMBER)
            {
                Common::RequestCode scaledCode = static_cast<Common::RequestCode>(static_cast<uint8_t>(rRequest.GetRequestCode()) + REQUEST_CODE_DIFFERENCE);
                Common::Request scaledReq(scaledCode, rRequest.GetData());
                HWTrackController::HWTrackControllerRequestManager reqManager;
                reqManager.HandleRequest(scaledReq, rResponse);
            }
            else
            {
                SWTrackController::serviceQueue.Push(rRequest);
                rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            }
            break;
        }
        case Common::RequestCode::END_DOWNLOAD:
        case Common::RequestCode::CREATE_TAG:
        case Common::RequestCode::CREATE_TASK:
        case Common::RequestCode::CREATE_ROUTINE:
        case Common::RequestCode::CREATE_RUNG:
        case Common::RequestCode::CREATE_INSTRUCTION:
            {
                Common::RequestCode scaledCode = static_cast<Common::RequestCode>(static_cast<uint8_t>(rRequest.GetRequestCode()) + REQUEST_CODE_DIFFERENCE);
                Common::Request scaledReq(scaledCode, rRequest.GetData());
                HWTrackController::HWTrackControllerRequestManager reqManager;
                reqManager.HandleRequest(scaledReq, rResponse);
            }
            else
            {
                SWTrackController::serviceQueue.Push(rRequest);
                rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            }
            break;
        }
        default:
            LOG_SW_TRACK_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace SWTrackController
