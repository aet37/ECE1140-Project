/**
 * @file Block.hpp
 */
#ifndef BLOCK_HPP
#define BLOCK_HPP

// SYSTEM INCLUDES
#include <string>
#include <vector>
#include "Station.hpp"
#include "Switch.hpp"

// FORWARD DECLARATIONS
class Station;
class Switch;

namespace TrackModel
{

/**
 * @class Block
 *
 * @brief Structure that holds data about a single block in a track
 */
class Block
{
public:
    Block(int blockNumber, double blockGrade, double blockSpeedLimit, std::string stationInfo, std::string switchInfo) :
        m_blockNumber(blockNumber),
        m_blockGrade(blockGrade),
        m_blockSpeedLimit(blockSpeedLimit),
        m_station(Station(stationInfo)),
        m_switch(Switch(switchInfo))
    {}

protected:
private:
    /// number of the block
    int m_blockNumber;

    /// grade of block
    double m_blockGrade;

    /// speed limit of block
    double m_blockSpeedLimit;

    /// station if applicable
    Station m_station;

    /// switch if applicable
    Switch m_switch;
};

} // namespace TrackModel

#endif