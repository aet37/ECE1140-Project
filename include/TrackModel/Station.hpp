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

        std::string getName()
        {
            return m_stationName;
        }
        std::string getExitSide()
        {
            return m_stationExitSide;
        }
        void setTicketsSold(int ticketsSold)
        {
            m_ticketsSold = ticketsSold;
        }
        int getTicketsSold()
        {
            return m_ticketsSold;
        }
        void setPassengers(int boarded, int exited)
        {
            m_passengersBoarded = m_passengersBoarded + boarded;
            m_passengersExited = m_passengersExited + exited;
        }
        int getPassengersBoarded()
        {
            return m_passengersBoarded;
        }
        int getPassengersExited()
        {
            return m_passengersExited;
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