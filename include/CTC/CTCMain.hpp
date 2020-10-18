/**
 * @file CTCMain.hpp
*/
#ifndef CTC_MAIN_HPP
#define CTC_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request
#include "TrainSystem.hpp"

namespace CTC
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();

} // namespace CTC

#endif // CTC_MAIN_HPP