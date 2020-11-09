/**
 * @file TrainCatalogue.hpp
 * 
 * @brief Declaration of the TrainCatalogue class
*/
#ifndef TRAIN_CATALOGUE_HPP
#define TRAIN_CATALOGUE_HPP

// SYSTEM INCLUDES
#include <vector>

// C++ PROJECT INCLUDES
#include "Train.hpp"

namespace TrainModel
{

/**
 * @class TrainCatalogue
 * 
 * @brief Repository for module's request managers
*/
class TrainCatalogue
{
public:
    /**
     * @brief Gets the singleton instance
    */
    static TrainCatalogue& GetInstance()
    {
        static TrainCatalogue* pInstance = new TrainCatalogue();
        return *(pInstance);
    }

    /**
     * @brief Gets a train from the list
    */
    Train* GetTrain(int trainId) const;

    /**
     * @brief Adds a train to the train list
    */
    void AddTrain(Train train, int trainId);

    /**
     * @brief Gets the number of trains in the list
    */
    std::size_t GetNumberOfTrains() const { return m_trainList.size(); }
    
protected:
private:
    /// List of trains
    std::vector<Train> m_trainList;

    /**
     * @brief Constructs a new TrainCatalogue object
     * 
     * @note Private to ensure singleton instance
    */
    TrainCatalogue() {}
};

} // namespace TrainModel

#endif // TRAIN_CATALOGUE_HPP
