/**
 * @file CTCMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "CTCMain.hpp" // Header for functions
#include "HWTrackControllerMain.hpp"
#include "Logger.hpp"

namespace CTC
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_CTC("In CTC main");
    LOG_CTC("Address of HWTrackController queue %x", &HWTrackController::serviceQueue);
    HWTrackController::serviceQueue.Push(Common::Request());
}

} // namespace CTC
