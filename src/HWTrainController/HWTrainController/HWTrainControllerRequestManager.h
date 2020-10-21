/**
 * @file HWTrainControllerRequestManager.hpp
 * 
 * @brief Declarations of the HWTrainControllerRequestManager class
*/
#ifndef HW_TRAIN_CONTROLLER_REQUEST_MANAGER_HPP
#define HW_TRAIN_CONTROLLER_REQUEST_MANAGER_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "RequestManagerIface.hpp" // For Common::RequestManagerIface
#include "ServiceQueue.hpp" // For Common::ServiceQueue

// FORWARD DECLARATIONS

namespace Common
{
class Response;
class Request;
}

namespace HWTrainController
{

/**
 * @class HWTrainControllerRequestManager
 * 
 * @brief This class is responsible for
 * handling requests to the hw Train controller
*/
class HWTrainControllerRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new HWTrainControllerRequestManager object
    */
    HWTrainControllerRequestManager() {}

    /**
     * @brief Handles the given request and constructs a response
     * 
     * @param[in] rRequest      Request to be handled
     * @param[out] rResponse    Response to the request 
    */
    void HandleRequest(const Common::Request& rRequest, Common::Response& rResponse);

protected:
private:
    /// Queue for requests to the hardware
    static Common::ServiceQueue<Common::Request*> m_requestQueue;

    /// Queue for responses from the hardware
    static Common::ServiceQueue<Common::Response*> m_responseQueue;

    /**
     * @brief Adds a request to the queue
    */
    void AddRequest(const Common::Request& rReq);

    /**
     * @brief Adds a response to the queue
    */
    void AddResponse(const Common::Response& rResp);

    /**
     * @brief Obtains the next request from the queue
    */
    Common::Request* GetNextRequest();

    /**
     * @brief Obtains the next response from the queue
    */
    Common::Response* GetNextResponse();
};

} // namespace HWTrainController

#endif // HW_TRAIN_CONTROLLER_REQUEST_MANAGER_HPP
