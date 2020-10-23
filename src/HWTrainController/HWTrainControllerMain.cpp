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

// send message to server, using send message function (send message with a request, goes to server, then the request manager picks it up and pushes it on to the queue for hardware)

} // namespace HWTrainController
