/**
 * @file Server.hpp
 *
 * @brief Declarations for the Server class
 */
#ifndef INCLUDE_SERVER_HPP_
#define INCLUDE_SERVER_HPP_

// SYSTEM INCLUDES
#include <boost/asio.hpp>

// C++ PROJECT INCLUDES
#include "ConnectionHandler.hpp" // For ConnectionHandler::pointer

// FORWARD DECLARATIONS
// (None)

/**
 * @class Server
 *
 * @brief Class to represent an Amazon Web Server
 */
class Server
{
public:
    /**
     * @brief Constructs a new Server object
     *
     * @param io_service
     */
    explicit Server(boost::asio::io_service& io_service) :
        m_acceptor(io_service, boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), 1304))
    {
        StartAccept();
    }

    /**
     * @brief Starts a connection if an error doesn't exist
     *
     * @param connection
     * @param rErr
     */
    void HandleAccept(ConnectionHandler::pointer connection, const boost::system::error_code& rErr);

protected:
private:
    /// Acceptor object for server
    boost::asio::ip::tcp::acceptor m_acceptor;

    /**
     * @brief Starts the asynchronous accept operation
     */
    void StartAccept();
};

#endif // INCLUDE_SERVER_HPP_
