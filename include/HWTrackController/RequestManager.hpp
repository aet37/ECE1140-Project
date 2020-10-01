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
struct Response;
struct Request;

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
     * @brief Adds a request to the queue
    */
    void AddRequest(Request& rRequest);

    /**
     * @brief Is there a request on the queue?
    */
    static bool IsRequest()
    {
        return !m_requestQueue.empty();
    }

protected:
private:
    /// Queue for requests to the hardware
    static std::queue<Request*> m_requestQueue;

    /// Queue for responses from the hardware
    static std::queue<Response*> m_responseQueue;

};

} // namespace HWTrackController

#endif // REQUEST_MANAGER_HPP