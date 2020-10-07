/**
 * @file ConnectionHandler.cpp
 * 
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <iostream>
#include <boost/bind.hpp>
#include <string>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class
#include "RequestManager.hpp" // For HWTrackController::RequestManager
#include "Request.hpp" // For Common::Request
#include "Response.hpp" // For Common::Response
#include "BufferFunctions.hpp"

#include "../CTC/TrainSystem.h"             // For CTC actions
#include "../../src/CTC/TrainSystem.cpp"

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
    std::cout << "Server received " << m_data << std::endl;

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
        std::cout << "Server sent " << m_message << std::endl;
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
        std::cerr << "Invalid command " << m_data << std::endl;
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
        	// Iterate through m_data to get destination block (first number in message)
        	std::string str_block;
        	str_block = rReq.GetData().substr(0, 2);

        	// Convert string to integer
        	int block_to = std::stoi(str_block);

			// Call TrainSystem singleton instance to create a new train
        	Train* pto_send;
        	pto_send = TrainSystem::GetInstance().create_new_train(block_to);

        	// Send Train Struct to Track Controller buffer function
	        TrainInfoBuffer_TC(pto_send->train_id, pto_send->destination_block, pto_send->authority, pto_send->command_speed);
            break;
        }
        default:
            std::cerr << "Invalid command " << m_data << " received" << std::endl;
            m_message = "INVALID COMMAND";
            return;
    }

    // Set the message, so the requester will receive the response
    m_message = resp.ToString();
}
