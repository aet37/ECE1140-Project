/**
 * @file BufferFunctions.hpp
 *
 * @brief Define buffer functions to communicate data between modules.
 * One buffer function per data communicated
 */
/*
 * Naming Convention of Buffer functions:
 *      DescriptionOfDataBuffer_Destination
 */

#include "TrainSystem.hpp" // For interactions with the train system
#include "TrackSystem.hpp"


/**
 * @brief	Buffer function to send info about new train from CTC to Track Controller
 *
 * @param[in]	train_id
 * @param[in]	destination_block
 * @param[in]	authority
 * @param[in]	command_speed
 *
 * @return	None
 */
void TrainInfoBuffer_TrackController(int train_id, int destination_block, int authority, int command_speed)
{
	TrackSystem::create_new_track(train_id, destination_block, authority, command_speed)
}

/**
 * @brief	Buffer function to send info about where the train is from Track controller to CTC
 *
 * @param[in]	block_location
 *
 * @return	None
 */
void TrainLocationBuffer_CTC(int block_location)
{
	TrainSystem::GetInstance().SetTrackOccupied(block_location);
	TrainSystem::GetInstance().SetTrackNotOccupied(block_location - 1);
}

void TrainLocationBuffer_SWTC(Track& a, int block_location)
{
    TrackSystem::updateoccupancies(a, block_location)

}

void SwitchPositionBuffer_TrackModel(int)
{



}

void TrainInfoBuffer_TrackModel(int train_id, int authority, int command_speed)
{


}