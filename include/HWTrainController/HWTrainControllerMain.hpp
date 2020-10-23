/**
 * @file HWTrainControllerMain.hpp
*/
#ifndef HW_TRAIN_CONTROLLER_MAIN_HPP
#define HW_TRAIN_CONTROLLER_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request

namespace HWTrainController
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();

} // namespace HWTrainController

#endif // HW_TRAIN_CONTROLLER_MAIN_HPP