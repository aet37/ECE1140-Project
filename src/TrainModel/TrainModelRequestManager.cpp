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
        {
            Train* pTrain = TrainCatalogue::GetInstance().GetTrain(rRequest.ParseData<uint32_t>(0));

            rResponse.AppendData(std::to_string(pTrain->GetDestinationBlock())); // 0
            rResponse.AppendData(std::to_string(pTrain->GetCommandSpeed())); // 1
            rResponse.AppendData(std::to_string(pTrain->GetCurrentSpeed())); // 2
            rResponse.AppendData(std::to_string(pTrain->GetPosition())); // 3
            rResponse.AppendData(std::to_string(pTrain->GetAuthority())); // 4
            rResponse.AppendData(std::to_string(pTrain->GetCurrentLine())); // 5
            rResponse.AppendData(std::to_string(pTrain->GetTempControl())); // 6
            rResponse.AppendData(std::to_string(pTrain->GetEmergencyPassengeBrake())); // 7
            rResponse.AppendData(std::to_string(pTrain->GetServiceBrake())); // 8
            rResponse.AppendData(std::to_string(pTrain->GetBrakeCommand())); // 9
            rResponse.AppendData(std::to_string(pTrain->GetHeadLights())); // 10
            rResponse.AppendData(std::to_string(pTrain->GetCabinLights())); // 11
            rResponse.AppendData(std::to_string(pTrain->GetAdvertisements())); // 12
            rResponse.AppendData(std::to_string(pTrain->GetAnnouncements())); // 13
            rResponse.AppendData(std::to_string(pTrain->GetDoors())); // 14
            rResponse.AppendData(std::to_string(pTrain->GetCurrentBlock())); // 15
            rResponse.AppendData(std::to_string(pTrain->GetMode())); // 16
            
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::TRAIN_MODEL_GUI_UPDATE_DROP_DOWN:
        {
            uint32_t numberOfTrains = TrainCatalogue::GetInstance().GetNumberOfTrains();
            rResponse.AppendData(std::to_string(numberOfTrains));
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
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
