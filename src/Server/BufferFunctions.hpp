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
	
}