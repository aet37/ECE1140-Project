/**
 * @file SWTrackControllerMain.hpp
*/
#ifndef SW_TRACK_CONTROLLER_MAIN_HPP
#define SW_TRACK_CONTROLLER_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request

namespace SWTrackController
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();

} // namespace SWTrackController

#endif // SW_TRACK_CONTROLLER_MAIN_HPP