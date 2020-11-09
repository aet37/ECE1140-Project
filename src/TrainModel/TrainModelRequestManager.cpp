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
#include "TrainCatalogue.hpp" // For

namespace TrainModel
{

void TrainModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    LOG_TRAIN_MODEL("RequestCode = %d", static_cast<uint8_t>(rRequest.GetRequestCode()));
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::TRAIN_MODEL_GUI_GATHER_DATA:
            Train* pTrain = TrainCatalogue::GetInstance().GetTrain(rRequest.ParseData<uint32_t>(0));

            rResponse.AppendData(std::to_string(pTrain->GetCommandSpeed()));
            rResponse.AppendData(std::to_string(pTrain->GetCurrentSpeed()));
            rResponse.AppendData(std::to_string(pTrain->GetPosition()));
            rResponse.AppendData(std::to_string(pTrain->GetAuthority()));
            rResponse.AppendData(std::to_string(pTrain->GetTempControl()));
            rResponse.AppendData(std::to_string(pTrain->GetEmergencyPassengeBrake()));
            rResponse.AppendData(std::to_string(pTrain->GetServiceBrake()));
            rResponse.AppendData(std::to_string(pTrain->GetBrakeCommand()));
            rResponse.AppendData(std::to_string(pTrain->GetHeadLights()));
            rResponse.AppendData(std::to_string(pTrain->GetCabinLights()));
            rResponse.AppendData(std::to_string(pTrain->GetAdvertisements()));
            rResponse.AppendData(std::to_string(pTrain->GetAnnouncements()));
            rResponse.AppendData(std::to_string(pTrain->GetDoors()));
            rResponse.AppendData(std::to_string(pTrain->GetCurrentBlock()));
            rResponse.AppendData(std::to_string(pTrain->GetMode()));
            
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
