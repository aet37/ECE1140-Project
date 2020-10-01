/**
 * @file ConnectionHandler.cpp
 * 
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <boost/bind.hpp>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class
#include "RequestManager.hpp"

void ConnectionHandler::Start()
{
    m_socket.async_read_some(boost::asio::buffer(m_data, ConnectionHandler::MAX_LENGTH),
                             boost::bind(&ConnectionHandler::HandleRead,
                             shared_from_this(),
                             boost::asio::placeholders::error,
                             boost::asio::placeholders::bytes_transferred));

    if (RequestManager::IsRequest())
    {
        m_message = "There's a request";
    }
    else
    {
        m_message = "fsfsdfs";
    }
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

    Command command;
    try
    {
        command = static_cast<Command>(std::stoi(m_data));
    }
    catch (std::exception& e)
    {
        std::cerr << "Invalid command " << m_data << std::endl;
        return;
    }

    HandleCommand(command);

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

void ConnectionHandler::HandleCommand(Command command)
{
    switch (command)
    {
        case COMMAND_GET_SWITCH_POSITION:
        {
            RequestManager rm;
            break;
        }
        default:
            std::cerr << "Invalid command " << command << " received";
            m_message = "Invalid Command " + command;
            break;
    }
}
