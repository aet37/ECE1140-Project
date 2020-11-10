/**
 * @file TrackModelRequestManager.cpp
 *
 * @brief Implementation of RequestManager class for Track Model Module
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cout

// C++ PROJECT INCLUDES
#include "TrackModelRequestManager.hpp" // Header for class 
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp"   // For logging (debugging)
#include "TrainSystem.hpp"  // For handling requests
#include "TrackModelMain.hpp"  // For acessing Service Queue

namespace TrackModel
{

int count = 0;
// FOR GUI STUFF
void TrackModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
		case Common::RequestCode::TRACK_MODEL_GUI_GATHER_DATA:
		{
			TrackModel::serviceQueue.Push(rRequest);
			rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
			break;
		}
		case Common::RequestCode::TRACK_MODEL_GUI_TRACK_LAYOUT:
		{
			TrackModel::serviceQueue.Push(rRequest);
			rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
			break;
		}
        case Common::RequestCode::TRACK_MODEL_GUI_BLOCK:
		{
			TrackModel::serviceQueue.Push(rRequest);
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