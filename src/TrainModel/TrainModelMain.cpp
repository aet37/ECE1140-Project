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
#include "BlockCatalogue.hpp" // For BlockCatalogue

namespace TrainModel
{

Common::ServiceQueue<Common::Request> serviceQueue;

    void moduleMain()
    {
        LOG_TRAIN_MODEL("Thread starting...");

        while (true)
        {
            Common::Request receivedRequest = serviceQueue.Pop();

            switch (receivedRequest.GetRequestCode())
            {
                case Common::RequestCode::TRAIN_MODEL_DISPATCH_TRAIN:
                {
                    Train newTrain;
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    newTrain.SetDestinationBlock(receivedRequest.ParseData<uint32_t>(1));
                    newTrain.SetCommandSpeed(receivedRequest.ParseData<uint32_t>(2));
                    newTrain.SetAuthority(receivedRequest.ParseData<uint32_t>(3));
                    newTrain.SetCurrentLine(receivedRequest.ParseData<uint32_t>(4));

                    // Parse through the remainder to construct this train's route
                    std::vector<uint32_t> route;
                    for (int i = 5; true; i++)
                    {
                        uint32_t block = 0;
                        try
                        {
                            block = receivedRequest.ParseData<uint32_t>(i);
                        }
                        catch (const std::exception& rException)
                        {
                            break;
                        }
                        route.push_back(block);
                    }
                    newTrain.SetRoute(route);

                    // Add the train to the catalogue
                    TrainCatalogue::GetInstance().AddTrain(newTrain);

                    // Prepare a request for Collin (trainId, destinationBlock, commandSpeed, authority)
                    Common::Request newRequest(Common::RequestCode::SWTRAIN_DISPATCH_TRAIN);
                    newRequest.AppendData(std::to_string(trainId));
                    newRequest.AppendData(std::to_string(receivedRequest.ParseData<uint32_t>(1)));
                    newRequest.AppendData(std::to_string(receivedRequest.ParseData<uint32_t>(2)));
                    newRequest.AppendData(std::to_string(receivedRequest.ParseData<uint32_t>(3)));
                    SWTrainController::serviceQueue.Push(newRequest);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_RECEIVE_BLOCK:
                {
                    LOG_TRAIN_MODEL("Train Model received %s", receivedRequest.GetData().c_str());
                    // Parse stuff from Evan (trackId, blockId, elevation, grade, length, speedLimit, travelDirection)
                    uint32_t trackId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t blockId = receivedRequest.ParseData<uint32_t>(1);

                    Block block;
                    block.m_elevation = receivedRequest.ParseData<float>(2);
                    block.m_slope = receivedRequest.ParseData<float>(3);
                    block.m_sizeOfBlock = receivedRequest.ParseData<uint32_t>(4);
                    block.m_speedLimit = receivedRequest.ParseData<uint32_t>(5);
                    block.m_travelDirection = receivedRequest.ParseData<uint32_t>(6);

                    // Add the block to the catalogue
                    if (trackId == 0)
                    {
                        BlockCatalogue::GetInstance().AddGreenBlock(block);
                        LOG_TRAIN_MODEL("Received a block. There are now %d blocks", BlockCatalogue::GetInstance().GetNumberOfGreenBlocks());
                    }
                    else
                    {
                        BlockCatalogue::GetInstance().AddRedBlock(block);
                        LOG_TRAIN_MODEL("Received a block. There are now %d blocks", BlockCatalogue::GetInstance().GetNumberOfRedBlocks());
                    }
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
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_LIGHTS:
                {
                    // // TESTING
                    // Train newTrain;
                    // Block newBlock;
                    // newBlock.m_elevation = 21;
                    // newBlock.m_slope = 8;
                    // newBlock.m_sizeOfBlock = 867;
                    // newBlock.m_accelerationLimit = 1;
                    // newBlock.m_decelerationLimit = 3;
                    // newBlock.m_speedLimit = 70;

                    // uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    // uint32_t lightStatus = receivedRequest.ParseData<uint32_t>(1);

                    // newTrain.SetCabinLights(lightStatus);
                    // TrainCatalogue::GetInstance().AddTrain(newTrain);
                    // BlockCatalogue::GetInstance().AddRedBlock(newBlock);

                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t lightStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetCabinLights(lightStatus);

                    LOG_TRAIN_MODEL("Train Cabin Lights = %d, Train ID = %d", lightStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_EBRAKE:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t eBrakeStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetEmergencyPassengeBrake(eBrakeStatus);

                    LOG_TRAIN_MODEL("Train eBrakeStatus = %d, Train ID = %d", eBrakeStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_SERVICE_BRAKE:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t serviceBrakeStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetServiceBrake(serviceBrakeStatus);

                    LOG_TRAIN_MODEL("Train serviceBrakeStatus = %d, Train ID = %d", serviceBrakeStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_DOORS:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t doorsStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetDoors(doorsStatus);

                    LOG_TRAIN_MODEL("Train doorsStatus = %d, Train ID = %d", doorsStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_SEAN_PAUL:
                {
                    // IMPLEMENTATION
                    // uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    // uint32_t seanPaulStatus = receivedRequest.ParseData<uint32_t>(1);

                    // Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId);
                    // tempTrain->SetCabinLights(seanPaulStatus);

                    // LOG_TRAIN_MODEL("Train seanPaulStatus = %d, Train ID = %d", seanPaulStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_ANNOUNCE_STATIONS:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    LOG_TRAIN_MODEL("Train Train ID = %d", trainId);
                    uint32_t announcementsStatus = receivedRequest.ParseData<uint32_t>(1);
                    LOG_TRAIN_MODEL("Train announcementsStatus = %d", announcementsStatus);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetAnnouncements(announcementsStatus);

                    LOG_TRAIN_MODEL("Train announcementsStatus = %d, Train ID = %d", announcementsStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_ADS:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t adsStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetAdvertisements(adsStatus);

                    LOG_TRAIN_MODEL("Train adsStatus = %d, Train ID = %d", adsStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_RESOLVE_FAILURE:
                {
                    // IMPLEMENTATION
                    // uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    // uint32_t lightStatus = receivedRequest.ParseData<uint32_t>(1);

                    // Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId);
                    // tempTrain->SetCabinLights(lightStatus);

                    // LOG_TRAIN_MODEL("Train Cabin Lights = %d, Train ID = %d", lightStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_RECEIVE_POWER:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t powerStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetPower(powerStatus);

                    LOG_TRAIN_MODEL("Train powerStatus = %d, Train ID = %d", powerStatus, trainId);
                    break;
                }
                case Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_MODE:
                {
                    // IMPLEMENTATION
                    uint32_t trainId = receivedRequest.ParseData<uint32_t>(0);
                    uint32_t modeStatus = receivedRequest.ParseData<uint32_t>(1);

                    Train *tempTrain = TrainCatalogue::GetInstance().GetTrain(trainId-1);
                    tempTrain->SetMode(modeStatus);

                    LOG_TRAIN_MODEL("Train modeStatus = %d, Train ID = %d", modeStatus, trainId);
                    break;
                }
                default:
                    ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(receivedRequest.GetRequestCode()));
            }
        }
    }

} // namespace TrainModel
