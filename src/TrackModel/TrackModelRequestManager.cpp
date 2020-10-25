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

void TrackModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        /*case Common::RequestCode::GET_POSITION_FROM_TRAINM:
        {
            // Add the request to the queue
            TrackModel::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
		case Common::RequestCode::SEND_TRACK_OCCUPANCY_TO_SW_TRACK_C:
		{
			TrackModel::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
		}*/
        /*case Common::RequestCode::CTC_SEND_GUI_OCCUPANCIES:
        {
        	// Temporary for Iteration 2
			if(count < 10)
			{
			    count++;
			}
			TrainSystem::GetInstance().SetTrackOccupied(count);
			if(count > 1)
			{
				TrainSystem::GetInstance().SetTrackNotOccupied(count - 1);
			}

			// send Response Code
	        rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);

			// Form response message; occupied = "t", not occupied = "f"
			std::string to_send;
			for(int i = 0; i < TrainSystem::GetInstance().GetTrackArr().size(); i++)
			{
			    if(TrainSystem::GetInstance().GetTrackArr()[i]->occupied)
			    {
			        to_send.push_back('t');
			    }
			    else
			    {
			        to_send.push_back('f');
			    }
			}
	        rResponse.SetData(to_send);

			// Log data sent
			LOG_CTC("From ConnectionHandler.cpp : Occupancies for each track sent");
            break;
        }*/
		case Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN:
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