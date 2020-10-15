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
#include "TrackSystem.h"

// Function prototypes for this file
void TrainInfoBuffer_CTC_TO_TrackController(int train_id, int destination_block, int authority, int command_speed);
void TrainInfoBuffer_TrainModel(int train_id, int authority, int command_speed, int current_speed, int speed_limit);
void SwitchPositionBuffer_TrackModel(int pos);
void TrainInfoBuffer_TrackModel(int train_id, int authority, int command_speed);
void TrainLocationBuffer_TC_TO_CTC(int block_location);
void TrainLocationBuffer_SWTC(int block_location);


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Destination: CTC
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * @brief	Buffer function to send info about where the train is from Track controller to CTC
 *
 * @param[in]	block_location
 *
 * @return	None
 */
void TrainLocationBuffer_TC_TO_CTC(int block_location)
{
	// set the block passed in as occupied
	TrainSystem::GetInstance().SetTrackOccupied(block_location);

	// set previous blocks as not occupied
	if(block_location == 1)
	{
		return;
	}
	else if(block_location == 11)
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(5);

		// Log what was done
		LOG_CTC("From TrainLocationBuffer_CTC() : Block %d set occupied, Block 5 set not occupied", block_location);
	}
	else
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(block_location - 1);

		// Log what was done
		LOG_CTC("From TrainLocationBuffer_CTC() : Block %d set occupied, Block %d set not occupied", block_location, block_location - 1);

	}
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Destination: Track Controller
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
void TrainInfoBuffer_CTC_TO_TrackController(int train_id, int destination_block, int authority, int command_speed)
{

	TrackSystem::GetInstance().create_new_track(train_id, destination_block, authority, command_speed);
	//TrainInfoBuffer_TrackModel(train_id, authority, command_speed);
	//SwitchPositionBuffer_TrackModel(TrackSystem::GetInstance().get_pos);
}

int count = 1;
void TrainLocationBuffer_SWTC(int block_location)
{
	//TrackSystem::GetInstance().update_occupancies(block_location);
	TrainLocationBuffer_TC_TO_CTC(block_location);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Destination: Train Model
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int tm_train_id, tm_authority, tm_command_speed, tm_current_speed, tm_speed_limit;
/**
 * @brief	Buffer function to send info about new train from
 *
 * @param[in]	train_id
 * @param[in]	authority
 * @param[in]	command_speed
 * @param[in]   current_speed
 * @param[in]   speed_limit
 *
 * @return	None
 */
void TrainInfoBuffer_TrainModel(int train_id, int authority, int command_speed, int current_speed, int speed_limit)
{
	tm_train_id = train_id;
	tm_authority = authority;
	tm_command_speed = command_speed;
	tm_current_speed = current_speed;
	tm_speed_limit = speed_limit;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Destination: Track Model
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void SwitchPositionBuffer_TrackModel(int pos)
{



}

void TrainInfoBuffer_TrackModel(int train_id, int authority, int command_speed)
{


}

