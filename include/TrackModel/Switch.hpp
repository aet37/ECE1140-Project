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