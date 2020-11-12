/**
 * @file BlockCatalogue.cpp
 *
 * @brief Implementations of the BlockCatalogue class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "BlockCatalogue.hpp" // Header for class
#include "Logger.hpp"

namespace TrainModel
{

Block* BlockCatalogue::GetBlock(int trackId, int blockId)
{
   if (trackId == 0)
   {
      return &m_greenBlockList[blockId];
   }
   else
   {
      return &m_redBlockList[blockId];
   }
}

void BlockCatalogue::AddGreenBlock(Block block)
{
   m_greenBlockList.push_back(block);
}

void BlockCatalogue::AddRedBlock(Block block)
{
   m_redBlockList.push_back(block);
}

} // namespace Common
