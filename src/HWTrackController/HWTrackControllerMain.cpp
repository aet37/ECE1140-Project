/**
 * @file HWTrackControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Logger.hpp"
#include "HWTrackControllerMain.hpp"

namespace HWTrackController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_HW_TRACK_CONTROLLER("Here");
    LOG_HW_TRACK_CONTROLLER("Address of my queue %x", &serviceQueue);
}

} // HWTrackController
