/**
 * @file TrackModelRequestManager.hpp
 * 
 * @brief Declarations of the TrackModelRequestManager class
*/
#ifndef TRACK_MODEL_REQUEST_MANAGER_HPP
#define TRACK_MODEL_REQUEST_MANAGER_HPP

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

namespace TrackModel
{

/**
 * @class TrackModelRequestManager
 * 
 * @brief This class is responsible for
 * handling requests for the Track Model
*/
class TrackModelRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new TrackModelRequestManager object
    */
    TrackModelRequestManager() {}

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

}

#endif