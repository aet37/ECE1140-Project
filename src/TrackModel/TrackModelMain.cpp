/**
 * @file TrackModelMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrackModelMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros

namespace TrackModel
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_TRACK_MODEL("Thread starting...");
}

} // namespace TrackModel
