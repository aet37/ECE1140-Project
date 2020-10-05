/**
 * @file RequestManager.hpp
 * 
 * @brief Declarations of the RequestManager class
*/
#ifndef REQUEST_MANAGER_HPP
#define REQUEST_MANAGER_HPP

// SYSTEM INCLUDES
#include <queue>

// C++ PROJECT INCLUDES
// (None)

// FORWARD DECLARATIONS

namespace Common
{
struct Response;
struct Request;
}

namespace HWTrackController
{

/**
 * @class RequestManager
 * 
 * @brief This class is responsible for
 * handling requests to the hw track controller
*/
class RequestManager
{
public:
    /**
     * @brief Constructs a new RequestManager object
    */
    RequestManager() {}

    /**
     * @brief Handles the given request and constructs a response
     * 
     * @param[in] rRequest      Request to be handled
     * @param[out] rResponse    Response to the request 
    */
    void HandleRequest(Common::Request& rRequest, Common::Response& rResponse);

protected:
private:
    /// Queue for requests to the hardware
    static std::queue<Common::Request*> m_requestQueue;

    /// Queue for responses from the hardware
    static std::queue<Common::Response*> m_responseQueue;

    /**
     * @brief Adds a request to the queue
    */
    void AddRequest(Common::Request& rReq);

    /**
     * @brief Adds a response to the queue
    */
    void AddResponse(Common::Response& rResp);

    /**
     * @brief Obtains the next request from the queue
    */
    Common::Request* GetNextRequest();

    /**
     * @brief Obtains the next response from the queue
    */
    Common::Response* GetNextResponse();
};

} // namespace HWTrackController

#endif // REQUEST_MANAGER_HPP
