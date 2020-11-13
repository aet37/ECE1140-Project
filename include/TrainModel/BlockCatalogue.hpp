/**
 * @file BlockCatalogue.hpp
 * 
 * @brief Declaration of the BlockCatalogue class
*/
#ifndef BLOCK_CATALOGUE_HPP
#define BLOCK_CATALOGUE_HPP

// SYSTEM INCLUDES
#include <vector>

// C++ PROJECT INCLUDES
// (None)

namespace TrainModel
{
/**
 * @struct Block
 * 
 * @brief Struct to store information about every block
 */
struct Block
{
    /// Elevation of block
    float m_elevation;

    /// Slope of the block
    float m_slope;

    /// Size of the block
    float m_sizeOfBlock;

    /// Acceleration limit of the block
    int m_accelerationLimit;

    /// Deceleration limit of the block
    int m_decelerationLimit;

    /// Speed limit of the block
    float m_speedLimit;

    /// Travel Direction
    /// TODO(KEM): Talk to Evan about this
    int m_travelDirection;
};

/**
 * @class BlockCatalogue
 * 
 * @brief Catalogue of all the blocks
*/
class BlockCatalogue
{
public:
    /**
     * @brief Gets the singleton instance
    */
    static BlockCatalogue& GetInstance()
    {
        static BlockCatalogue* pInstance = new BlockCatalogue();
        return *(pInstance);
    }

    /**
     * @brief Gets a block from the catalogue
     * 
     * @param trackId       Id of the track to get the block from
     * @param blockId       Index of the block to get
    */
    Block* GetBlock(int trackId, int blockId);

    /**
     * @brief Adds a block to the end of the block list
     * 
     * @param block     Block to be added
    */
    void AddGreenBlock(Block block);

    /**
     * @brief Adds a block to the end of the block list
     * 
     * @param block     Block to be added
    */
    void AddRedBlock(Block block);

    /**
     * @brief Gets the number of blocks in green track
    */
    std::size_t GetNumberOfGreenBlocks() const { return m_greenBlockList.size(); }

    /**
     * @brief Gets the number of blocks in red track
    */
    std::size_t GetNumberOfRedBlocks() const { return m_redBlockList.size(); }
    
protected:
private:
    /// List of blocks on the green line
    std::vector<Block> m_greenBlockList;

    /// List of blocks on the red line
    std::vector<Block> m_redBlockList;

    /**
     * @brief Constructs a new BlockCatalogue object
     * 
     * @note Private to ensure singleton instance
    */
    BlockCatalogue() {}
};

} // namespace TrainModel

#endif // BLOCK_CATALOGUE_HPP
