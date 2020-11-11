/**
 * @file SWTrackControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrackControllerMain.hpp" // Header for functions
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // For LOG macros
#include "TrackModelMain.hpp"
#include "CTCMain.hpp"

namespace SWTrackController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_SW_TRACK_CONTROLLER("Thread starting...");

    while(true)
    {
        Common::Request receivedReq = serviceQueue.Pop();

    	switch(receivedReq.GetRequestCode())
        {
            case Common::RequestCode::SWTRACK_DISPATCH_TRAIN:
            {
                // Parse stuff from the CTC
                uint32_t trainId = receivedReq.ParseData<uint32_t>(0);
                uint32_t destinationBlock = receivedReq.ParseData<uint32_t>(1);
                uint32_t suggestedSpeed = receivedReq.ParseData<uint32_t>(2);
                uint32_t authority = receivedReq.ParseData<uint32_t>(3);
                uint32_t line = receivedReq.ParseData<uint32_t>(4);
                std::string switchPositions = receivedReq.ParseData<std::string>(5);

                // Do some processing
                // TODO

                // Pass information to Track Model
                Common::Request newReq(Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN);
                newReq.AppendData(receivedReq.ParseData<std::string>(0));
                newReq.AppendData(receivedReq.ParseData<std::string>(1));
                newReq.AppendData(receivedReq.ParseData<std::string>(2));
                newReq.AppendData(receivedReq.ParseData<std::string>(3));
                newReq.AppendData(receivedReq.ParseData<std::string>(4));
                newReq.AppendData(receivedReq.ParseData<std::string>(5));
                TrackModel::serviceQueue.Push(newReq);
                LOG_SW_TRACK_CONTROLLER("SWTrackController dispatch train %d", trainId);
                break;
            }
            case Common::RequestCode::SWTRACK_UPDATE_AUTHORITY:
            case Common::RequestCode::SWTRACK_SET_TRACK_SIGNAL:
            case Common::RequestCode::SWTRACK_UPDATE_COMMAND_SPEED:
            case Common::RequestCode::SWTRACK_SET_TRACK_STATUS:
            case Common::RequestCode::SWTRACK_SET_SWITCH_POSITION:
            case Common::RequestCode::SWTRACK_SET_TRACK_FAILURE:
            case Common::RequestCode::SWTRACK_SET_TRACK_OCCUPANCY:
            case Common::RequestCode::SWTRACK_SET_CROSSING:
            case Common::RequestCode::SWTRACK_SET_TRACK_HEATER:
            case Common::RequestCode::START_DOWNLOAD:
            case Common::RequestCode::END_DOWNLOAD:
            case Common::RequestCode::CREATE_TAG:
            case Common::RequestCode::CREATE_TASK:
            case Common::RequestCode::CREATE_ROUTINE:
            case Common::RequestCode::CREATE_RUNG:
            case Common::RequestCode::CREATE_INSTRUCTION:
            case Common::RequestCode::SET_TAG_VALUE:
            case Common::RequestCode::GET_TAG_VALUE:
            default:
                ASSERT(false, "Unhandled request code %d", static_cast<uint16_t>(receivedReq.GetRequestCode()));
                break;
        }
    }
}

} // namespace SWTrackController
