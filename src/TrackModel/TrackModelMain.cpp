/**
 * @file TrackModelMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrackModelMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"
#include "SWTrackControllerMain.hpp"

namespace TrackModel
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_TRACK_MODEL("Thread starting...");

    while (true)
    {
        Common::Request req = serviceQueue.Pop();

        switch(req.GetRequestCode())
        {
            case Common::RequestCode::GET_POSITION_FROM_TRAINM: 
            {
                uint32_t position = std::stoi(req.GetData());

                std::string occupancy_send = std::to_string(position);
                
                Common::Request newRequest(Common::RequestCode::SWTRACK_GET_OCCUPANCY, occupancy_send);
                SWTrackController::serviceQueue.Push(newRequest);
                // Recieve position in ??? units from Train Model
                // Hardcoding to 75 units for now
                //req.SetData("75");
                break;
            }
            case Common::RequestCode::SEND_TRACK_OCCUPANCY_TO_SW_TRACK_C:
            {
                
                break;

            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }


    }



}

} // namespace TrackModel
