/**
 * @file TrackModelMain.hpp
*/
#ifndef TRACK_MODEL_MAIN_HPP
#define TRACK_MODEL_MAIN_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "ServiceQueue.hpp" // For Common::ServiceQueue
#include "Request.hpp" // For Request

namespace TrackModel
{

extern Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain();
void initializeRouteMaps();

} // namespace TrackModel

#endif // TRACK_MODEL_MAIN_HPP
