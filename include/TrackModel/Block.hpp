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
    Block(int blockNumber, double blockLength, double blockGrade, int blockSpeedLimit, double blockElevation, 
    double blockCumulativeElevation, std::string blockDirection, std::string blockUnderground, 
    std::string stationInfo, std::string switchInfo, std::string blockRailwayCrossing)
    {
        m_blockNumber = blockNumber;
        m_blockLength = blockLength;
        m_blockGrade = blockGrade;
        m_blockSpeedLimit = blockSpeedLimit;
        m_blockElevation = blockElevation;
        m_blockCumulativeElevation = blockCumulativeElevation;
        m_blockDirection = blockDirection;
        m_blockUnderground = blockUnderground;
        m_blockRailwayCrossing = blockRailwayCrossing;

        if (stationInfo != "")
        {
            m_theStation = Station(stationInfo);
            m_stationBool = true;
        }
        else
        {
            m_stationBool = false;
        }

        if (switchInfo != "")
        {
            m_theSwitch = Switch(switchInfo);
            m_switchBool = true;
        }
        else 
        {
            m_switchBool = false;
        }
        
    }

protected:
private:
    /// number of the block
    int m_blockNumber;

    /// length of block
    double m_blockLength;

    /// grade of block
    double m_blockGrade;

    /// speed limit of block
    int m_blockSpeedLimit;

    /// elevation of the block
    double m_blockElevation;

    /// cumulative elevation of block
    double m_blockCumulativeElevation;

    /// travel direction of block
    std::string m_blockDirection;

    ///is block underground
    std::string m_blockUnderground;

    /// station on the block, "" if none exists
    //std::string m_stationInfo;
    Station m_theStation;

    /// is there a station on this block?
    bool m_stationBool;

    /// switch on the block, "" if none exists
    //std::string m_switchInfo;
    Switch m_theSwitch;

    bool m_switchBool;

    /// railway crossing on block
    std::string m_blockRailwayCrossing;



};

} // namespace TrackModel

#endif