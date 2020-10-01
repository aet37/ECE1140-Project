/**
 * @file ConnectionHandler.cpp
 * 
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <boost/bind.hpp>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class
#include "RequestManager.hpp" // For HWTrackController::RequestManager
#include "Request.hpp" // For Request

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
    std::cout << m_data << std::endl;

    // Parse the data into the request structure
    Request req;
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
        std::cout << "Server sent Hello Message!" << std::endl;
    }
    else
    {
        std::cerr << "error: " << rErr.message() << std::endl;
        m_socket.close();
    }
}

void ConnectionHandler::ParseRequest(Request& rReq)
{
    try
    {
        rReq.reqCode = static_cast<RequestCode>(std::stoi(m_data));
    }
    catch (std::exception& e)
    {
        std::cerr << "Invalid command " << m_data << std::endl;
        rReq.reqCode = RequestCode::ERROR;
    }
}

void ConnectionHandler::HandleRequest(Request& rReq)
{
    switch (rReq.reqCode)
    {
        case RequestCode::SET_SWITCH_POSITION:
        {
            HWTrackController::RequestManager rm;
            rm.AddRequest(rReq);
            break;
        }
        case RequestCode::CHECK_FOR_HW_TRACK_CONTROLLER_REQUEST:
            std::cout << HWTrackController::RequestManager::IsRequest() << std::endl;
            m_message = HWTrackController::RequestManager::IsRequest();
            break;
        default:
            std::cerr << "Invalid command " << rReq.reqCode << " received" << std::endl;
            m_message = "INVALID COMMAND";
            break;
    }
}
