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
    Station()
    {

    }
    
    Station(std::string stationInfo)
    {
        
        int pos = stationInfo.find(",");
        m_stationName = stationInfo.substr(0, pos);

        stationInfo.erase(0, pos + 1);

        m_stationExitSide = stationInfo;

        printf("\n\n");
        printf(m_stationName.c_str());
        printf("\n\n");
        printf(m_stationExitSide.c_str());
        printf("\n\n");

        // stationInfo.erase(0, 12);
        // int pos = stationInfo.find('\"'); // HERRON AVE", "Exit Side": "Right"
        // std::string name = stationInfo.substr(0, pos);
        // m_stationName = name;

        // stationInfo.erase(0, pos + 17);
        // pos = stationInfo.find('\"');
        // std::string exitSide = stationInfo.substr(0, pos);
        // m_stationExitSide = exitSide;

        m_ticketsSold = 0;
        m_passengersBoarded = 0;
        m_passengersExited = 0;

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