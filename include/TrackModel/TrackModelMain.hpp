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
//void initializeRouteMaps(std::map<std::string, std::vector<uint32_t>> test1, std::map<std::string, std::vector<uint32_t>> test2);

} // namespace TrackModel

#endif // TRACK_MODEL_MAIN_HPP
