/**
 * @file SWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrainControllerMain.hpp" // Header for functions
#include "TrainModelMain.hpp"
#include "Logger.hpp" // For LOG macros

namespace SWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_SW_TRAIN_CONTROLLER("Thread starting...");

    Common::Request req(Common::RequestCode::TRAIN_MODEL_GIVE_POWER, "5");

    TrainModel::serviceQueue.Push(req);

    Common::Request receivedReq = serviceQueue.Pop();

    LOG_TRAIN_MODEL("We received something!!! %s", receivedReq.GetData().c_str());
}

} // namespace SWTrainController
