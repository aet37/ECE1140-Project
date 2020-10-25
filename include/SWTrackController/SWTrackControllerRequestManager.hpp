/**
 * @file SWTrackControllerRequestManager.hpp
 * 
 * @brief Declarations of the SWTrackControllerRequestManager class
*/
#ifndef SW_TrackController_REQUEST_MANAGER_HPP
#define SW_TrackController_REQUEST_MANAGER_HPP

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

namespace SW_TrackController
{

/**
 * @class SWTrackControllerRequestManager
 * 
 * @brief This class is responsible for
 * handling requests for the SW Track Controller
*/
class SWTrackControllerRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new SWTrackControllerRequestManager object
    */
    SWTrackControllerRequestManager() {}

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

} // namespace SWTrackController

#endif // SW_TrackController_REQUEST_MANAGER_HPP
