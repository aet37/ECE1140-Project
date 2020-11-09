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
    int m_elevation;

    /// Slope of the block
    int m_slope;

    /// Size of the block
    int m_sizeOfBlock;

    /// Acceleration limit of the block
    int m_accelerationLimit;

    /// Deceleration limit of the block
    int m_decelerationLimit;

    /// Speed limit of the block
    int m_speedLimit;

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
     * @param blockId       Index of the block to get
    */
    Block* GetBlock(int blockId);

    /**
     * @brief Adds a block to the end of the block list
     * 
     * @param block     Block to be added
    */
    void AddBlock(Block block);

    /**
     * @brief Gets the number of blocks in the list
    */
    std::size_t GetNumberOfBlocks() const { return m_blockList.size(); }
    
protected:
private:
    /// List of blocks
    std::vector<Block> m_blockList;

    /**
     * @brief Constructs a new BlockCatalogue object
     * 
     * @note Private to ensure singleton instance
    */
    BlockCatalogue() {}
};

} // namespace TrainModel

#endif // BLOCK_CATALOGUE_HPP
