/**
 * @file TrainModelMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrainModelMain.hpp" // Header for functions
#include "SWTrainControllerMain.hpp" // For SWTrainController::serviceQueue
#include "TrainModelData.hpp" // For TrainModel::tm_current_speed
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // For LOG macros

namespace TrainModel
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_TRAIN_MODEL("Thread starting...");
    int currentSpeed;

    while (true)
    {
        Common::Request receivedRequest = serviceQueue.Pop();

        switch (receivedRequest.GetRequestCode())
        {
            case Common::RequestCode::TRAIN_MODEL_GIVE_POWER:
            {
                uint32_t power = std::stoi(receivedRequest.GetData());
                currentSpeed = (power * 2);
                LOG_TRAIN_MODEL("currentSpeed = %d", currentSpeed);
                std::string currentSpeedSend = std::to_string(currentSpeed);
                Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED, currentSpeedSend);
                SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_DISPATCH_TRAIN:
            {
                uint32_t disData = std::stoi(receivedRequest.GetData());
                LOG_TRAIN_MODEL("Dispatch Train = %d", currendisDatatSpeed);
                std::string disDataSend = std::to_string(disData);
                Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN, disDataSend);
                SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(receivedRequest.GetRequestCode()));
        }
    }
}

} // namespace TrainModel
