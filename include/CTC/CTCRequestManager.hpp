/**
 * @file CTCRequestManager.hpp
 * 
 * @brief Declarations of the CTCRequestManager class
*/
#ifndef CTC_REQUEST_MANAGER_HPP
#define CTC_REQUEST_MANAGER_HPP

// SYSTEM INCLUDES
#include <queue>

// C++ PROJECT INCLUDES
#include "RequestManagerIface.hpp" // For Common::RequestManagerIface

// FORWARD DECLARATIONS

namespace Common
{
struct Response;
struct Request;
}

namespace CTC
{

/**
 * @class CTCRequestManager
 * 
 * @brief This class is responsible for
 * handling requests for the CTC
*/
class CTCRequestManager : public Common::RequestManagerIface
{
public:
    /**
     * @brief Constructs a new CTCRequestManager object
    */
    CTCRequestManager() {}

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

} // namespace CTC

#endif // CTC_REQUEST_MANAGER_HPP
