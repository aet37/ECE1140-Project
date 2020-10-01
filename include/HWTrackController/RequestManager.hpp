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
     * @struct Request
     * 
     * @brief Structure to hold request information
    */
    typedef struct Request
    {
        
    } Request;

    /**
     * @struct Response
     * 
     * @brief Structure to hold response information
    */
    typedef struct Response
    {

    } Response;

    /**
     * @brief Constructs a new RequestManager object
    */
    RequestManager() {}

    /**
     * @brief Adds a request to the queue
    */
    void AddRequest(Request* pRequest);

    /**
     * 
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

#endif // REQUEST_MANAGER_HPP