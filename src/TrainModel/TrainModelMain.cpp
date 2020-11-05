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
                LOG_TRAIN_MODEL("Dispatch Train = %d", disData);
                std::string disDataSend = std::to_string(disData);
                Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN, disDataSend);
                SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_GATHER_DATA:
            {
                // uint32_t power = std::stoi(receivedRequest.GetData());
                // currentSpeed = (power * 2);
                // LOG_TRAIN_MODEL("currentSpeed = %d", currentSpeed);
                // std::string currentSpeedSend = std::to_string(currentSpeed);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_AUTHORITY, currentSpeedSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_UPDATE_AUTHORITY:
            {
                uint32_t Authority = std::stoi(receivedRequest.GetData());
                // Calculate Update here
                LOG_TRAIN_MODEL("Authority = %d", Authority);
                std::string AuthoritySend = std::to_string(Authority);
                Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_AUTHORITY, AuthoritySend);
                SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_UPDATE_COMMAND_SPEED:
            {
                uint32_t commandSpeed = std::stoi(receivedRequest.GetData());
                // Calculate Update here
                LOG_TRAIN_MODEL("commandSpeed = %d", commandSpeed);
                std::string commandSpeedSend = std::to_string(commandSpeed);
                Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_COMMAND_SPEED, commandSpeedSend);
                SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_SET_THE_DAMN_LIGHTS:
            {
                uint32_t theLights = std::stoi(receivedRequest.GetData());
                LOG_TRAIN_MODEL("Lights Status = %d", theLights);
                std::string theLightsSend = std::to_string(theLights);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN, theLightsSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_CAUSE_FAILURE:
            {
                // uint32_t power = std::stoi(receivedRequest.GetData());
                // currentSpeed = (power * 2);
                // LOG_TRAIN_MODEL("currentSpeed = %d", currentSpeed);
                // std::string currentSpeedSend = std::to_string(currentSpeed);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED, currentSpeedSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_LENGTH:
            {
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t trainLength = receivedRequest.ParseData<uint32_t>(1);
                LOG_TRAIN_MODEL("Train Length = %d\nTrain ID = %d", trainLength, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_MASS:
            {
                // uint32_t power = std::stoi(receivedRequest.GetData());
                // currentSpeed = (power * 2);
                // LOG_TRAIN_MODEL("currentSpeed = %d", currentSpeed);
                // std::string currentSpeedSend = std::to_string(currentSpeed);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED, currentSpeedSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT:
            {
                // uint32_t disData = std::stoi(receivedRequest.GetData());
                // LOG_TRAIN_MODEL("Dispatch Train = %d", currendisDatatSpeed);
                // std::string disDataSend = std::to_string(disData);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN, disDataSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_WIDTH:
            {
                // uint32_t power = std::stoi(receivedRequest.GetData());
                // currentSpeed = (power * 2);
                // LOG_TRAIN_MODEL("currentSpeed = %d", currentSpeed);
                // std::string currentSpeedSend = std::to_string(currentSpeed);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED, currentSpeedSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT:
            {
                // uint32_t disData = std::stoi(receivedRequest.GetData());
                // LOG_TRAIN_MODEL("Dispatch Train = %d", currendisDatatSpeed);
                // std::string disDataSend = std::to_string(disData);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN, disDataSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT:
            {
                // uint32_t disData = std::stoi(receivedRequest.GetData());
                // LOG_TRAIN_MODEL("Dispatch Train = %d", currendisDatatSpeed);
                // std::string disDataSend = std::to_string(disData);
                // Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN, disDataSend);
                // SWTrainController::serviceQueue.Push(newRequest);
                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(receivedRequest.GetRequestCode()));
        }
    }
}

} // namespace TrainModel
