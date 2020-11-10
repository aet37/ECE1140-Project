/**
 * @file Station.hpp
 */
#ifndef SWITCH_HPP
#define SWITCH_HPP

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
class Switch
{
public:
    Switch()
    {

    }
    Switch(std::string switchInfo)
        //m_switchBlocks(switchBlocks),
        //m_currentBlock(switchBlocks[0])
    {
        int pos = switchInfo.find(" ");
        int switch1 = std::stoi(switchInfo.substr(0, pos));
        switchInfo.erase(0, pos + 1);
        int switch2 = std::stoi(switchInfo);

        if (switch1 > switch2)
        {
            int switch3 = switch2;
            switch2 = switch1;
            switch1 = switch3;
        }

        m_switchBlocks.push_back(switch1);
        m_switchBlocks.push_back(switch2);

        m_currentBlock = m_switchBlocks[0];

    }

protected:
private:
    /// list of blocks the switch could be pointing to
    std::vector<int> m_switchBlocks;

    /// the block the switch is currently pointing to
    int m_currentBlock;

};

} // namespace TrackModel

#endif