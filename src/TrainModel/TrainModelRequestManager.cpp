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
#include "BlockCatalogue.hpp" // For

namespace TrainModel
{

void TrainModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    LOG_TRAIN_MODEL("RequestCode = %d", static_cast<uint8_t>(rRequest.GetRequestCode()));
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::TRAIN_MODEL_GUI_1_GATHER_DATA:
        {
            Train* pTrain = TrainCatalogue::GetInstance().GetTrain(rRequest.ParseData<uint32_t>(0) - 1);
            Block* pBlock = BlockCatalogue::GetInstance().GetBlock(pTrain->GetCurrentLine(), pTrain->GetCurrentBlock());

            rResponse.AppendData(std::to_string(pTrain->GetCommandSpeed())); // 0
            rResponse.AppendData(std::to_string(pTrain->GetAuthority())); // 1
            rResponse.AppendData(std::to_string(pTrain->GetCurrentSpeed())); // 2
            rResponse.AppendData(std::to_string(pBlock->m_speedLimit)); // 3
            //rResponse.AppendData(std::to_string(3)); // 3
            rResponse.AppendData(std::to_string(pTrain->GetBrakeCommand())); // 4
            rResponse.AppendData(std::to_string(pTrain->GetServiceBrake())); // 5
            rResponse.AppendData(std::to_string(pTrain->GetEmergencyPassengeBrake())); // 6
            rResponse.AppendData(std::to_string(pTrain->GetCurrentLine())); // 7
            
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::TRAIN_MODEL_GUI_2_GATHER_DATA:
        {
            Train* pTrain = TrainCatalogue::GetInstance().GetTrain(rRequest.ParseData<uint32_t>(0) - 1);
            Block* pBlock = BlockCatalogue::GetInstance().GetBlock(pTrain->GetCurrentLine(), pTrain->GetCurrentBlock());

            rResponse.AppendData(std::to_string(pBlock->m_accelerationLimit)); // 0
            rResponse.AppendData(std::to_string(pBlock->m_decelerationLimit)); // 1
            rResponse.AppendData(std::to_string(pBlock->m_elevation)); // 2
            rResponse.AppendData(std::to_string(pBlock->m_slope)); // 3
            // Position calculated in gui
            rResponse.AppendData(std::to_string(pBlock->m_sizeOfBlock)); // 4
            rResponse.AppendData(std::to_string(pTrain->GetCurrentBlock())); // 5
            rResponse.AppendData(std::to_string(pTrain->GetDestinationBlock())); // 6
            
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::TRAIN_MODEL_GUI_3_GATHER_DATA:
        {
            Train* pTrain = TrainCatalogue::GetInstance().GetTrain(rRequest.ParseData<uint32_t>(0) - 1);
            Block* pBlock = BlockCatalogue::GetInstance().GetBlock(pTrain->GetCurrentLine(), pTrain->GetCurrentBlock());

            rResponse.AppendData(std::to_string(pTrain->GetTrainPassCount())); // 0
            rResponse.AppendData(std::to_string(pTrain->GetTrainCrewCount())); // 1
            rResponse.AppendData(std::to_string(pTrain->GetAnnouncements())); // 2
            rResponse.AppendData(std::to_string(pTrain->GetAdvertisements())); // 2
            rResponse.AppendData(std::to_string(pTrain->GetCabinLights())); // 4
            rResponse.AppendData(std::to_string(pTrain->GetHeadLights())); // 5
            rResponse.AppendData(std::to_string(pTrain->GetTempControl())); // 6
            rResponse.AppendData(std::to_string(pTrain->GetDoors())); // 7

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
