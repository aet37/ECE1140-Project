/**
 * @file DebugRequestManager.hpp
 * 
 * @brief Declarations of the DebugRequestManager class
*/
#ifndef DEBUG_REQUEST_MANAGER_HPP
#define DEBUG_REQUEST_MANAGER_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "RequestManagerIface.hpp" // For Common::RequestManagerIface

// FORWARD DECLARATIONS

namespace Common
{
class Response;
class Request;
}

namespace Debug
{

/**
 * @class DebugRequestManager
 * 
 * @brief This class will be used to simulate data
 * being passed from module to module
*/
class DebugRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new HWTrackControllerRequestManager object
    */
    DebugRequestManager() {}

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

} // namespace Debug

#endif // DEBUG_REQUEST_MANAGER_HPP
