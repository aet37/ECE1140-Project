/**
 * @file SWTrainControllerMain.hpp
*/
#ifndef SW_TRAIN_CONTROLLER_MAIN_HPP
#define SW_TRAIN_CONTROLLER_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request

namespace SWTrainController
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();

} // namespace SWTrainController

#endif // SW_TRAIN_CONTROLLER_MAIN_HPP
