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
#include "Track.hpp" // For TrackModel::Track
#include "Logger.hpp"       // For logging events (debugging purposes)

namespace TrackModel
{

/**
* @brief Read in the layout of the track
 *
* @param std::string line, std::vector<Station> stations, std::vector<Switch> switches, int totalBlocks, std::vector<Block> blockList
*
* @return int trackNumber
*
*/
void TrackInfo::AddTrackLayout(std::string line, int number, int totalBlocks)
{
    //Eventaully will add checks to make sure same line tracks aren't added


    Track* pNewTrack = new Track(line, number, totalBlocks);

    m_pTrackList.push_back(pNewTrack);
    //Track *newTrack = new Track();
    //pNewTrack->m_line = line;
    //pNewTrack->m_number = number;
    //pNewTrack->m_totalBlocks = totalBlocks;

    //trackList.push_back(newTrack);

	LOG_TRACK_MODEL("From TrackInfo::AddTrackLayout() : %d Track Created: Track ", m_pTrackList.size());
}

Track* TrackInfo::getTrack(int trackNumber)
{
    return m_pTrackList[trackNumber - 1];
}

} // namespace TrackModel
