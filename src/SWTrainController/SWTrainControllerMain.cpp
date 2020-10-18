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
}

} // namespace SWTrainController
