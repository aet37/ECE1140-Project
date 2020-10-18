/**
 * @file HWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrainControllerMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros

namespace HWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_HW_TRAIN_CONTROLLER("Thread starting...");
}

} // namespace HWTrainController
