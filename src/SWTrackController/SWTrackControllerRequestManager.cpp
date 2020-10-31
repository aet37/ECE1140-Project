#include <iostream>

#include "SWTrackControllerRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp"   // For logging (debugging)
#include "TrackSystem.hpp"  // For handling requests
#include "SWTrackControllerMain.hpp"  // For acessing Service Queue

namespace SW_TrackController
{


    void SWTrackControllerRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
    {
        switch(rRequest.GetRequestCode())
        {
            case Common::RequestCode:: SWTRACK_DISPATCH_TRAIN:
            {
                SWTrackController::serviceQueue.Push(rRequest);
                rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
                break;





            }

            default:
            std::cerr << "Invalid command " << static_cast<uint16_t>(rRequest.GetRequestCode())
                      << " received" << std::endl;
            rResponse.SetData("INVALID COMMAND");
            return;














        }
    }
}