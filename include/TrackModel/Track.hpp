/**
 * @file Track.hpp
 */
#ifndef TRACK_HPP
#define TRACK_HPP

// SYSTEM INCLUDES
#include <string>
#include <vector>

// FORWARD DECLARATIONS
class Station;
class Switch;
class Block;

namespace TrackModel
{

/**
 * @class Track
 *
 * @brief Structure that holds data about a single track
 */
class Track
{
public:
    Track(std::string lineColor, int totalBlocks, int blockNumber) :
        m_line(lineColor),
        m_totalBlocks(totalBlocks),
        m_number(blockNumber)
        // m_stations(),
        // m_switches(),
        // m_blockList()
    {}

    void AddBlock(std::string test)
    {
        


    }

protected:
private:
    /// Color of the line
    std::string m_line;

    ///
    int m_totalBlocks;

    ///
    int m_number;

    ///
    // std::vector<Station> m_stations;

    // instead of station vector, int vector of blocks they're on
    // std::vector<Switch> m_switches;

    // instead of switch vector, int vector of blocks they're on
    // std::vector<Block> m_blockList;
};

} // namespace TrackModel

#endif