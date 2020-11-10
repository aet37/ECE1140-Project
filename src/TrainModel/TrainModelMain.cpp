/**
 * @file TrainModelMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrainModelMain.hpp" // Header for functions
#include "SWTrainControllerMain.hpp" // For SWTrainController::serviceQueue
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // For LOG macros
#include "Train.hpp" // For TrainModel::Train
#include "TrainCatalogue.hpp" // For TrainCatalogue

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
                Train newTrain;
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                newTrain.SetDestinationBlock(receivedRequest.ParseData<uint32_t>(1));
                newTrain.SetCommandSpeed(receivedRequest.ParseData<uint32_t>(2));
                newTrain.SetAuthority(receivedRequest.ParseData<uint32_t>(3));
                newTrain.SetCurrentLine(receivedRequest.ParseData<uint32_t>(4));
                // Route info from Evan? receivedRequest.ParseData<uint32_t>(5);


                TrainCatalogue::GetInstance().AddTrain(newTrain);

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
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                bool theLights = receivedRequest.ParseData<bool>(1);
                LOG_TRAIN_MODEL("Train Light Status = %d, Train ID = %d", theLights, trainId);
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
                LOG_TRAIN_MODEL("Train Length = %d, Train ID = %d", trainLength, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_MASS:
            {
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t trainMass = receivedRequest.ParseData<uint32_t>(1);
                LOG_TRAIN_MODEL("Train Mass = %d, Train ID = %d", trainMass, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT:
            {
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t trainHeight = receivedRequest.ParseData<uint32_t>(1);
                LOG_TRAIN_MODEL("Train Height = %d, Train ID = %d", trainHeight, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_WIDTH:
            {
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t trainWidth = receivedRequest.ParseData<uint32_t>(1);
                LOG_TRAIN_MODEL("Train Width = %d, Train ID = %d", trainWidth, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT:
            {
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t trainPassengerCount = receivedRequest.ParseData<uint32_t>(1);
                LOG_TRAIN_MODEL("Train Passenger Count = %d, Train ID = %d", trainPassengerCount, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT:
            {
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t trainCrewCount = receivedRequest.ParseData<uint32_t>(1);
                LOG_TRAIN_MODEL("Train Crew Count = %d, Train ID = %d", trainCrewCount, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_UPDATE_DROP_DOWN:
            {
                //uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                //uint32_t trainPassengerCount = receivedRequest.ParseData<uint32_t>(1);
                //LOG_TRAIN_MODEL("Train Passenger Count = %d, Train ID = %d", trainPassengerCount, trainId);
                break;
            }
            case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_LIGHTS:
            {
                // TESTING
                Train newTrain;
                uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                uint32_t lightStatus = receivedRequest.ParseData<uint32_t>(1);

                newTrain.SetCabinLights(lightStatus);
                TrainCatalogue::GetInstance().AddTrain(newTrain);

                // IMPLEMENTATION
                // uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                // uint32_t lightStatus = receivedRequest.ParseData<uint32_t>(1);

                // Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId);
                // tempTrain->SetCabinLights(lightStatus);

                LOG_TRAIN_MODEL("Train Cabin Lights = %d, Train ID = %d", lightStatus, trainId);
                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(receivedRequest.GetRequestCode()));
        }
    }
}

} // namespace TrainModel
