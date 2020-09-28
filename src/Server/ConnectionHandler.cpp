/**
 * @file ConnectionHandler.cpp
 * 
 * @brief Implementation of the ConnectionHandler class
 */

// SYSTEM INCLUDES
#include <boost/bind.hpp>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // Header for class

void ConnectionHandler::Start()
{
    m_socket.async_read_some(boost::asio::buffer(m_data, ConnectionHandler::MAX_LENGTH),
                             boost::bind(&ConnectionHandler::HandleRead,
                             shared_from_this(),
                             boost::asio::placeholders::error,
                             boost::asio::placeholders::bytes_transferred));

    m_socket.async_write_some(boost::asio::buffer(m_message, ConnectionHandler::MAX_LENGTH),
                              boost::bind(&ConnectionHandler::HandleWrite,
                              shared_from_this(),
                              boost::asio::placeholders::error,
                              boost::asio::placeholders::bytes_transferred));
}

void ConnectionHandler::HandleRead(const boost::system::error_code& rErr, size_t bytesTransferred)
{
    if (!rErr)
    {
        // Just print out the received data
        std::cout << m_data << std::endl;
    }
    else
    {
        std::cerr << "error: " << rErr.message() << std::endl;
        m_socket.close();
    }
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
