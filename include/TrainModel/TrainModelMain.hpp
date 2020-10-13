/**
 * @file TrainModelMain.hpp
*/
#ifndef TRAIN_MODEL_MAIN_HPP
#define TRAIN_MODEL_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request

namespace TrainModel
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();

} // namespace TrainModel

#endif // TRAIN_MODEL_MAIN_HPP