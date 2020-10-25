/**
 * @file TrackInfo.cpp
 *
 * @brief Implementations of the TrackInfo class
 *
 * @author Evan Kutney
 *
 * @date 10.17.2020
 *
*/

#include "TrackInfo.hpp"  // Definition of class
// #include <vector>           // For accessing list of Trains, Tracks, Signals
#include "Logger.hpp"       // For logging events (debugging purposes)
static std::vector<Track> trackList;


/**
* @brief Read in the layout of the track
 *
* @param std::string line, std::vector<Station> stations, std::vector<Switch> switches, int totalBlocks, std::vector<Block> blockList
*
* @return int trackNumber
*
*/
void TrackInfo::AddTrackLayout(std::string line, /*std::vector<Station> stations, std::vector<Switch> switches,*/ int totalBlocks, std::vector<Block> blockList)
{
    //Eventaully will add checks to make sure same line tracks aren't added
    Track newTrack;
    newTrack.m_line = line;
    //newTrack.m_stations = stations;
    //newTrack.m_switches = switches;
    newTrack.m_totalBlocks = totalBlocks;
	newTrack.m_blockList = blockList;

    trackList.push_back(newTrack);

	LOG_TRACK_MODEL("From TrackInfo::AddTrackLayout() : %d Track Created: Track ", trackList.size());
}