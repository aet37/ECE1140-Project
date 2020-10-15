/**
 * @file TrainModelRequestManager.cpp
 *
 * @brief Implementation of RequestManager class for TrainModel Module
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrainModelRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp"   // For LOG macros

namespace TrainModel
{

void TrainModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    LOG_TRAIN_MODEL("RequestCode = %d", static_cast<uint8_t>(rRequest.GetRequestCode()));
    switch (rRequest.GetRequestCode())
    {
        default:
            LOG_TRAIN_MODEL("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace TrainModel
