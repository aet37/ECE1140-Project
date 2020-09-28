/**
 * @file Server.cpp
 *
 * @brief Implementation of the Server class
 */

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Server.hpp" // Header for class

void Server::HandleAccept(ConnectionHandler::pointer connection, const boost::system::error_code& rErr)
{
    if (!rErr)
    {
        connection->Start();
    }
    StartAccept();
}

void Server::StartAccept()
{
    // socket
    ConnectionHandler::pointer connection = ConnectionHandler::create(m_acceptor.get_io_service());

    // asynchronous accept operation and wait for a new connection
    m_acceptor.async_accept(connection->Socket(),
                            boost::bind(&Server::HandleAccept, this, connection,
                            boost::asio::placeholders::error));
}