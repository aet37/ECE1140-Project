/**
 * @file DebugRequestManager.cpp
 *
 * @brief Implementation of DebugRequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "DebugRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros

namespace Debug
{

void DebugRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    // Common::RequestCode reqCode = std::stoi(rRequest.GetData());


    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::DEBUG_TO_CTC:

            break;
        default:
            LOG_DEBUG("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace Debug
