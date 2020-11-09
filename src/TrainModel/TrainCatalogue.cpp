/**
 * @file TrainCatalogue.cpp
 *
 * @brief Implementations of the TrainCatalogue class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrainCatalogue.hpp" // Header for class

namespace TrainModel
{

/**
 * @brief Gets a train from the list
*/
Train* TrainCatalogue::GetTrain(int trainId) const
{
   return &m_trainList[trainId];
}

/**
 * @brief Adds a train to the train list
*/
void TrainCatalogue::AddTrain(Train train, int trainId) const
{
   m_trainList[trainId] = train; // ?????????????????????????????????????????????
}

} // namespace Common
