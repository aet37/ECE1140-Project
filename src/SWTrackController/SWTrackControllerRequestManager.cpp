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
            case Common::RequestCode::
        }
    }
}