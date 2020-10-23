/**
 * @file HWTrainRequestManager.hpp
 * 
 * @brief Declarations of the HWTrainRequestManager class
*/
#ifndef HW_TRAIN_CONTROLLER
#define HW_TRAIN_CONTROLLER

// SYSTEM INCLUDES
#include <queue>

// C++ PROJECT INCLUDES
#include "RequestManagerIface.hpp" // For Common::RequestManagerIface

// FORWARD DECLARATIONS

namespace Common
{
class Response;
class Request;
}

namespace HWTrainController
{

/**
 * @class HWTrainRequestManager
 * 
 * @brief This class is responsible for
 * handling requests for the HWTrainController
*/
class HWTrainRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new HWTrainRequestManager object
    */
    HWTrainRequestManager() {}

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

} // namespace HWTrainController

#endif // HW_TRAIN_CONTROLLER
