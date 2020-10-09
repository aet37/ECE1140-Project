/**
 * @file ConnectionHandler.cpp
 * 
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <iostream>
#include <boost/bind.hpp>
#include <string>
#include <vector>
#include <bits/stdc++.h> 
#include <boost/algorithm/string.hpp> 

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class
#include "RequestManager.hpp" // For HWTrackController::RequestManager
#include "Request.hpp" // For Common::Request
#include "Response.hpp" // For Common::Response
#include "BufferFunctions.hpp"
#include "TrainModelData.hpp" // For TrainModel::setTrainLength
#include "Logger.hpp" // For LOG macros

#include "TrainSystem.hpp"             // For CTC actions
#include "TrackSystem.h"

#include "TrackModelData.hpp"

void ConnectionHandler::Start()
{
    m_socket.async_read_some(boost::asio::buffer(m_data, ConnectionHandler::MAX_LENGTH),
                             boost::bind(&ConnectionHandler::HandleRead,
                             shared_from_this(),
                             boost::asio::placeholders::error,
                             boost::asio::placeholders::bytes_transferred));
}

void ConnectionHandler::HandleRead(const boost::system::error_code& rErr, size_t bytesTransferred)
{
    if (rErr)
    {
        std::cerr << "error: " << rErr.message() << std::endl;
        m_socket.close();
        return;
    }

    // Terminate what was transferred
    m_data[bytesTransferred] = '\0';

    // Just print out the received data
    LOG_SERVER("Server received %s", m_data);

    // Parse the data into the request structure
    Common::Request req;
    ParseRequest(req);

    // Determine what needs done for this request
    HandleRequest(req);

    m_socket.async_write_some(boost::asio::buffer(m_message, ConnectionHandler::MAX_LENGTH),
                              boost::bind(&ConnectionHandler::HandleWrite,
                              shared_from_this(),
                              boost::asio::placeholders::error,
                              boost::asio::placeholders::bytes_transferred));
}

void ConnectionHandler::HandleWrite(const boost::system::error_code& rErr, size_t bytesTransferred)
{
    if (!rErr)
    {
        // Just print out a message
        LOG_SERVER("Server sent %s", m_message.c_str());
    }
    else
    {
        std::cerr << "error: " << rErr.message() << std::endl;
        m_socket.close();
    }
}

void ConnectionHandler::ParseRequest(Common::Request& rReq)
{
    try
    {
        // Convert data to an string
        std::string data = std::string(m_data);

        std::string requestCode = "";
        std::string additionalData = "";
        if (data.find_first_of(" ") == std::string::npos)
        {
            requestCode = data;
        }
        else
        {
            requestCode = data.substr(0, data.find_first_of(" "));
            additionalData = data.substr(data.find_first_of(" ") + 1);
        }

        // First characters should be the request code
        rReq.SetRequestCode(static_cast<Common::RequestCode>(std::stoi(requestCode)));

        // Place the additional data into the data field of the request
        rReq.SetData(additionalData);
    }
    catch (std::exception& e)
    {
        LOG_SERVER("Invalid command %s", m_data);
        rReq.SetRequestCode(Common::RequestCode::ERROR);
    }
}

void ConnectionHandler::HandleRequest(Common::Request& rReq)
{
    Common::Response resp;
    switch (rReq.GetRequestCode())
    {
        case Common::RequestCode::SET_SWITCH_POSITION:
        case Common::RequestCode::GET_SWITCH_POSITION:
        {
            resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            resp.SetData("6");
            break;
        }
        case Common::RequestCode::GET_HW_TRACK_CONTROLLER_REQUEST:
        case Common::RequestCode::SEND_HW_TRACK_CONTROLLER_RESPONSE:
        case Common::RequestCode::GET_HW_TRACK_CONTROLLER_RESPONSE:
       
        {
            HWTrackController::RequestManager rm;
            rm.HandleRequest(rReq, resp);
            break;
        }
        case Common::RequestCode::CTC_DISPATCH_TRAIN:
        {
        	// Extract the block train was dispatched to
        	std::string str_block = rReq.GetData().substr(0, 2);

        	// Convert block to integer
        	int block_to = std::stoi(str_block);

			// Call TrainSystem singleton instance to create a new train
        	Train* pto_send;
        	pto_send = TrainSystem::GetInstance().CreateNewTrain(block_to);

        	// Send Train Struct to Track Controller buffer function
	        TrainInfoBuffer_CTC_TO_TrackController(pto_send->train_id, pto_send->destination_block, pto_send->authority, pto_send->command_speed);

	        // Log action
	        LOG_CTC("From ConnectionHandler.cpp (CTC_DISPATCH_TRAIN) : Sent Track C. Train %d to block %d", pto_send->train_id, pto_send->destination_block);

	        // Make pointer null
	        pto_send = nullptr;
            break;
        }
	    case Common::RequestCode::CTC_SEND_OCCUPANCIES:
	    {
	    	// Update Track location
		    TrainLocationBuffer_SWTC(count);    // Send location to SWTC

			if(count < 10)
			{
				count++;
			}

	    	// send Response Code
			resp.SetResponseCode(Common::ResponseCode::SUCCESS);

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
			resp.SetData(to_send);

			// Log data sent
			LOG_CTC("From ConnectionHandler.cpp : Occupancies for each track sent");

			break;
	    }
        case Common::RequestCode::GET_COMMAND_SPEED:
        {
            resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            resp.SetData("45");
            break;
        }
        case Common::RequestCode::GET_SIGNAL_TIMES:
        {
            TrackModel::setSpeedLimit(std::stoi(rReq.GetData())); //irrelevant speed limit

            //TrackModel::getBlockNumber();
            
            
            resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            int block = TrackModel::getBlockNumber();
            TrainLocationBuffer_SWTC(block);
            resp.SetData(std::to_string(block));

            /*resp.AppendData("11:59");
            resp.AppendData("12:00");
            resp.AppendData("12:01");
            resp.AppendData("12:02");
            resp.AppendData("12:03");
            resp.AppendData("12:04");
            resp.AppendData("12:05");
            resp.AppendData("12:06");
            resp.AppendData("12:07");
            resp.AppendData("12:08");
            resp.AppendData("12:09");
            resp.AppendData("12:10");
            resp.AppendData("12:11");
            resp.AppendData("12:12");*/

            //resp.AppendData("30");
            //resp.AppendData("40");
            break;
        }
        case Common::RequestCode::SET_SPEED_LIMIT:
        {
            TrackModel::setSpeedLimit(std::stoi(rReq.GetData()));
            resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::GET_SPEED_LIMIT:
        {
            resp.SetData(std::to_string(TrackModel::getSpeedLimit()));
            resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        
        case Common::RequestCode::SET_TRAIN_LENGTH:
        {
            std::vector<std::string> result; 
            boost::split(result, rReq.GetData(), boost::is_any_of(" ")); 
            TrainModel::TrainInfoBuffer_TrainModel(std::stoi(result[0]),
                                                    std::stoi(result[1]),
                                                    std::stoi(result[2]),
                                                    std::stoi(result[3]),
                                                    std::stoi(result[4]));

            resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SEND_TRAIN_MODEL_DATA:
        {
            // TrainModel::TrainInfoBuffer_TrainModel(std::stoi(rReq.GetData()));
            // resp.SetResponseCode(Common::ResponseCode::SUCCESS);
            // break;
        }
        case Common::RequestCode::SWTRACK_OCCUPANCY_TO_CTC:
        {
           int occupancy= TrackSystem::GetInstance().get_track_occ();
           TrainLocationBuffer_TC_TO_CTC(occupancy);
           break;
        }
        case Common::RequestCode::SWTRACK_SWITCHPOSITION_TO_TRAINM:
        {

        }
        case Common::RequestCode::SWTRACK_TRACKSIGNAL_TO_TRAINM:
        {

        }
        default:
            LOG_SERVER("Invalid RequestCode %d", static_cast<int>(rReq.GetRequestCode()));
            resp.SetResponseCode(Common::ResponseCode::ERROR);
            break;
    }

    // Set the message, so the requester will receive the response
    m_message = resp.ToString();
}
