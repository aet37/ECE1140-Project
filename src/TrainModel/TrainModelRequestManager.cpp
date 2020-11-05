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
#include "TrainModelMain.hpp" // For TrainModel::serviceQueue

namespace TrainModel
{

void TrainModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    LOG_TRAIN_MODEL("RequestCode = %d", static_cast<uint8_t>(rRequest.GetRequestCode()));
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::TRAIN_MODEL_GUI_GATHER_DATA:
            // Temporarily hard code the current speed
            rResponse.SetData("10");
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_LENGTH:
        case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_MASS:
        case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT:
        case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT:
        case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_WIDTH:
        case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT:
            TrainModel::serviceQueue.Push(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        default:
            LOG_TRAIN_MODEL("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

} // namespace TrainModel
