/**
 * @file BlockCatalogue.cpp
 *
 * @brief Implementations of the BlockCatalogue class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "BlockCatalogue.hpp" // Header for class

namespace TrainModel
{

Block* BlockCatalogue::GetBlock(int blockId) const
{
   return &m_blockList[blockId];
}

void BlockCatalogue::AddBlock(Block block)
{
   m_blockList.push_back(block);
}

} // namespace Common
