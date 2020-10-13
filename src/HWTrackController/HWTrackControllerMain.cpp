/**
 * @file HWTrackControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrackControllerMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros

namespace HWTrackController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_HW_TRACK_CONTROLLER("Thread starting...");
}

} // HWTrackController
