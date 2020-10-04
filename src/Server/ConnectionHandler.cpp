/**
 * @file ConnectionHandler.cpp
 * 
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <iostream>
#include <boost/bind.hpp>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class
#include "RequestManager.hpp" // For HWTrackController::RequestManager
#include "Request.hpp" // For Common::Request
#include "Response.hpp" // For Common::Response

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
    std::cout << "Server recieved " << m_data << std::endl;

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
        rReq.SetRequestCode(static_cast<Common::RequestCode>(std::stoi(m_data)));

        std::string data = std::string(&m_data[2]);
        rReq.SetData(data);
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
        case Common::RequestCode::GET_HW_TRACK_CONTROLLER_REQUEST:
        {
            HWTrackController::RequestManager rm;
            rm.HandleRequest(rReq, resp);
            break;
        }
        default:
            std::cerr << "Invalid command " << m_data << " received" << std::endl;
            m_message = "INVALID COMMAND";
            return;
    }

    m_message = resp.ToString();
}
