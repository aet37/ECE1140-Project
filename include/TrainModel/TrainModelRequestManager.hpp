/**
 * @file TrainModelRequestManager.hpp
 * 
 * @brief Declarations of the TrainModelRequestManager class
*/
#ifndef TRAIN_MODEL_REQUEST_MANAGER_HPP
#define TRAIN_MODEL_REQUEST_MANAGER_HPP

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

namespace TrainModel
{

/**
 * @class TrainModelRequestManager
 * 
 * @brief This class is responsible for
 * handling requests for the Train Model
*/
class TrainModelRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new TrainModelRequestManager object
    */
    TrainModelRequestManager() {}

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

} // namespace TrainModel

#endif // TRAIN_MODEL_REQUEST_MANAGER_HPP
