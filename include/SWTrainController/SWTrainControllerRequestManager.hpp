/**
 * @file SWTrainControllerRequestManager.hpp
 * 
 * @brief Declarations of the SWTrainControllerRequestManager class
*/
#ifndef SW_TRAIN_CONTROLLER_REQUEST_MANAGER_HPP
#define SW_TRAIN_CONTROLLER_REQUEST_MANAGER_HPP

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

namespace SWTrainController
{

/**
 * @class SWTrainControllerRequestManager
 * 
 * @brief This class is responsible for
 * handling requests to the sw train controller
*/
class SWTrainControllerRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new SWTrainControllerRequestManager object
    */
    SWTrainControllerRequestManager() {}

    /**
     * @brief Handles the given request and constructs a response
     * 
     * @param[in] rRequest      Request to be handled
     * @param[out] rResponse    Response to the request 
    */
    void HandleRequest(const Common::Request& rRequest, Common::Response& rResponse);

protected:
private:
};

} // namespace SWTrainController

#endif // SW_TRAIN_CONTROLLER_REQUEST_MANAGER_HPP
