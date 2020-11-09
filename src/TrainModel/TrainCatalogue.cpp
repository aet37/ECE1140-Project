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

Train* TrainCatalogue::GetTrain(int trainId)
{
   return &m_trainList[trainId];
}

/**
 * @brief Adds a train to the train list
*/
void TrainCatalogue::AddTrain(Train train)
{
   m_trainList.push_back(train);
}

} // namespace Common
