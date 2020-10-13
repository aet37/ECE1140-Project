/**
 * @file HWTrackControllerMain.hpp
*/
#ifndef HW_TRACK_CONTROLLER_MAIN_HPP
#define HW_TRACK_CONTROLLER_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request

namespace HWTrackController
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();

} // namespace HWTrackController

#endif // HW_TRACK_CONTROLLER_MAIN_HPP