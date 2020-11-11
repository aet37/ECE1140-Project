/**
 * @file TrackModelDef.hpp
 *
 * @brief Declaration of Structs in Track Model
 *
 * @author Evan Kutney
 *
 * @date 10.17.2020
*/
#ifndef TRACKMODEL_TRACKMODELDEF_H
#define TRACKMODEL_TRACKMODELDEF_H

#include <vector>
#include <string>




/**
 * @struct Block
 *
 * @brief Structure that holds data about a single block
 *
 */
struct Block
{
    std::string m_section;
    int m_blockNumber;
    int m_blockGrade;
    int m_speedLimit;
    int m_station;
    int m_switch;
    int m_elevation;
    int m_cumulativeElevation;
    // bool m_trackHeater
    // int m_occupiedByTrain
    // int m_directionOfTravel
    // bool m_railwayCrossing
    // TODO: add stuff from the class diagram
};

/**
 * @struct Station
 *
 * @brief Structure that holds data about a single station
 *
 */
struct Station
{
    // may not need blockNumber at all
    int m_blockNumber;
    std::string m_stationName;
    // int m_ticketsSold
    // int m_passengersBoarded
    // int m_passengersExited
};

/**
 * @struct Switch
 *
 * @brief Structure that holds data about a single switch
 *
 */
struct Switch
{
    // may  not need blockLocation at all???
    int m_blockLocation;
    std::vector<int> switchToBlocks;
    // int m_switchPointingTowards
};

#endif
