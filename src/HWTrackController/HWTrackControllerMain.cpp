/**
 * @file HWTrackControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrackControllerMain.hpp" // Header for functions
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // For LOG macros

namespace HWTrackController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_HW_TRACK_CONTROLLER("Thread starting...");

    while (true)
    {
        Common::Request receivedRequest = serviceQueue.Pop();

        switch (receivedRequest.GetRequestCode())
        {
            case Common::RequestCode::SWTRACK_GET_TRACK_SIGNAL:
            {
                
                break;
            }
            default:
                ASSERT(false, "Unexpected request received %d", static_cast<uint16_t>(receivedRequest.GetRequestCode()));
                break;
        }
    }
}

} // namespace HWTrackController
