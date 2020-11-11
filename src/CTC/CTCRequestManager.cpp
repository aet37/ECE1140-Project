/**
 * @file CTCRequestManager.cpp
 *
 * @brief Implementation of RequestManager class for CTC Module
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cout

// C++ PROJECT INCLUDES
#include "CTCRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp"   // For logging (debugging)
#include "TrainSystem.hpp"  // For handling requests
#include "CTCMain.hpp"  // For acessing Service Queue

namespace CTC
{

// Temporary for Iteration 2
int count = 0;

void CTCRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::CTC_GUI_DISPATCH_TRAIN:
        {
            // Add the request to the queue
            CTC::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::CTC_SEND_GUI_GREEN_OCCUPANCIES: {
	        // send Response Code
	        rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);

	        // Form response message; occupied = "t", not occupied = "f"
	        std::string to_send;

	        // Add green line blocks
	        for (int i = 0; i < TrainSystem::GetInstance().GetTrackArr(LINE_GREEN).size(); i++) {
		        if (TrainSystem::GetInstance().GetTrackArr(LINE_GREEN)[i]->occupied) {
			        to_send.push_back('t');
		        } else {
			        to_send.push_back('f');
		        }
	        }
	        rResponse.SetData(to_send);

	        // Log data sent
	        LOG_CTC("From ConnectionHandler.cpp : Occupancies for each track on GREEN LINE sent");
	        break;
        }
	    case Common::RequestCode::CTC_SEND_GUI_RED_OCCUPANCIES:
	    {
		    // send Response Code
		    rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);

		    // Form response message; occupied = "t", not occupied = "f"
		    std::string to_send;

		    // Add green line blocks
		    for(int i = 0; i < TrainSystem::GetInstance().GetTrackArr(LINE_RED).size(); i++)
		    {
			    if(TrainSystem::GetInstance().GetTrackArr(LINE_RED)[i]->occupied)
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
		    LOG_CTC("From ConnectionHandler.cpp : Occupancies for each track on RED LINE sent");
		    break;
	    }
	    case Common::RequestCode::CTC_SEND_GUI_SWITCH_POS_GREEN:
	    {
		    // send Response Code
		    rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);

		    // Form response message
		    std::string to_send;

		    // Add green line switches
		    for(int i = 0; i < TrainSystem::GetInstance().GetSwitchesArr(LINE_GREEN).size(); i++)
		    {
			    to_send.append(TrainSystem::GetInstance().GetSwitchesArr(LINE_GREEN)[i]->TrackSwitchToString());
			    if(i != TrainSystem::GetInstance().GetSwitchesArr(LINE_GREEN).size() - 1)
			    {
				    to_send.append(" ");
			    }
		    }
		    rResponse.SetData(to_send);

		    // Log data sent
		    LOG_CTC("From ConnectionHandler.cpp : Switches on GREEN LINE sent");
		    break;
	    }
	    case Common::RequestCode::CTC_SEND_GUI_SWITCH_POS_RED:
	    {
		    // send Response Code
		    rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);

		    // Form response message
		    std::string to_send;

		    // Add green line switches
		    for(int i = 0; i < TrainSystem::GetInstance().GetSwitchesArr(LINE_RED).size(); i++)
		    {
			    to_send.append(TrainSystem::GetInstance().GetSwitchesArr(LINE_RED)[i]->TrackSwitchToString());
			    if(i != TrainSystem::GetInstance().GetSwitchesArr(LINE_RED).size() - 1)
			    {
				    to_send.append(" ");
			    }
		    }
		    rResponse.SetData(to_send);

		    // Log data sent
		    LOG_CTC("From ConnectionHandler.cpp : Switches on Red LINE sent");
		    break;
	    }
    	case Common::RequestCode::CTC_SEND_GUI_VAILD_TRAIN:
	    {
	    	bool in_system = false;
	    	int tnum = std::stoi(rRequest.GetData());

	    	for (int i = 0; i < TrainSystem::GetInstance().GetTrainArr().size(); i++)
		    {
	    		if (tnum == TrainSystem::GetInstance().GetTrainArr()[i]->train_id)
			    {
	    			in_system = true;
			    }
		    }

	    	if (in_system)
		    {
			    rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
		    }
	    	else
		    {
			    rResponse.SetResponseCode(Common::ResponseCode::ERROR);
		    }
			break;
	    }
        default:
            std::cerr << "Invalid command " << static_cast<uint16_t>(rRequest.GetRequestCode())
                      << " received" << std::endl;
            rResponse.SetData("INVALID COMMAND");
            return;
    }
}
} // namespace HWTrackController
