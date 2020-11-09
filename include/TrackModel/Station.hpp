/**
 * @file Station.hpp
 */
#ifndef STATION_HPP
#define STATION_HPP

// SYSTEM INCLUDES
#include <string>
#include <vector>

namespace TrackModel
{

/**
 * @class Station
 *
 * @brief Structure that holds data about a single station in a block
 */
class Station
{
public:
    Station(std::string stationInfo) :
        m_ticketsSold(0),
        m_passengersBoarded(0),
        m_passengersExited(0)
    {
        stationInfo.erase(0, 12);
        int pos = stationInfo.find('\"'); // HERRON AVE", "Exit Side": "Right"
        std::string name = stationInfo.substr(0, pos);
        m_stationName = name;

        stationInfo.erase(0, pos + 17);
        pos = stationInfo.find('\"');
        std::string exitSide = stationInfo.substr(0, pos);
        m_stationExitSide = exitSide;
        }

protected:
private:
    /// name of station
    std::string m_stationName;

    /// side the station is exited on
    std::string m_stationExitSide;

    /// tickets sold per station per day
    int m_ticketsSold;

    /// Total passengers boarded per day
    int m_passengersBoarded;

    /// Total passengers exited per day
    int m_passengersExited;

};

} // namespace TrackModel

#endif