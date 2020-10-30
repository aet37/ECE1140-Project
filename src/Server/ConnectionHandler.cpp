/**
 * @file ConnectionHandler.cpp
 *
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <iostream>
#include <string>
#include <vector>
#include <boost/bind.hpp>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class
#include "Request.hpp" // For Common::Request
#include "Response.hpp" // For Common::Response
#include "RequestManagerIface.hpp" // For Common::RequestManagerIface
#include "RequestManagerRepository.hpp" // For Common::RequestManagerRepository
#include "Logger.hpp" // For LOG macros


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

    // Return early if the request code is ERROR
    if (rReq.GetRequestCode() == Common::RequestCode::ERROR)
    {
        resp.SetResponseCode(Common::ResponseCode::ERROR);
        m_message = resp.ToString();
        return;
    }


    // Get the module-specific request manager from the repository
    Common::RequestManagerRepository& rRepo = Common::RequestManagerRepository::GetInstance();
    Common::RequestManagerIface* pReqManager = rRepo.GetRequestManager(rReq.GetRequestCode());

    // Allow the specific request manager to handle it
    pReqManager->HandleRequest(rReq, resp);

    // Set the message, so the requester will receive the response
    m_message = resp.ToString();
}
