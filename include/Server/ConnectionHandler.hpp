/**
 * @file ConnectionHandler.hpp
*/
#ifndef INCLUDE_CONNECTION_HANDLER_HPP_
#define INCLUDE_CONNECTION_HANDLER_HPP_

// SYSTEM INCLUDES
#include <boost/asio.hpp>
#include <boost/enable_shared_from_this.hpp>

// C++ PROJECT INCLUDES
// (None)

// FORWARD DECLARATIONS
struct Request;

class ConnectionHandler : public boost::enable_shared_from_this<ConnectionHandler>
{
public:
    typedef boost::shared_ptr<ConnectionHandler> pointer;

    /**
     * @brief Creates a new ConnectionHandler object
    */
    ConnectionHandler(boost::asio::io_service& rIoService) :
        m_socket(rIoService)
    {}

    /**
     * @brief Creates the pointer
    */
    static pointer Create(boost::asio::io_service& rIoService)
    {
            return pointer(new ConnectionHandler(rIoService));
    }

    /**
     * @brief Returns the socket member
    */
    boost::asio::ip::tcp::socket& GetSocket()
    {
        return m_socket;
    }

    /**
     * @brief Begins an asynchronous read and write one after another
     * 
     * @details If you would like to alter how read and writes are handled,
     * edit HandleRead and HandleWrite. If you would like to change when or in
     * what order, this method can be altered
    */
    void Start();

    /**
     * @brief Method to operate on the data read from the client
     * 
     * @param rErr                  Error if applicable
     * @param bytesTransferred      Number of bytes transferred from client
    */
    void HandleRead(const boost::system::error_code& rErr, size_t bytesTransferred);

    /**
     * @brief Method to perform tasks after sending data to client
     * 
     * @param rErr                  Error if applicable
     * @param bytesTransferred      Number of bytes transferred to client
    */
    void HandleWrite(const boost::system::error_code& rErr, size_t bytesTransferred);

protected:
private:
    /// TCP socket
    boost::asio::ip::tcp::socket m_socket;

    /// Message (Server -> Client)
    std::string m_message = "Hello From Server!";

    /// Max length of message
    static const uint32_t MAX_LENGTH = 1024;

    /// Data (Client -> Server)
    char m_data[MAX_LENGTH];

    /**
     * 
    */
    void ParseRequest(Request& rReq);

    /**
     * @brief Determines what actions to take for a given request. This
     * could include setting the reply message
     * 
     * @param rReq   Request that was received
    */
    void HandleRequest(Request& rReq);
};

#endif // INCLUDE_CONNECTION_HANDLER_HPP_