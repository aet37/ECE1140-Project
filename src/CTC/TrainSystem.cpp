/**
 * @file TrainSystem.cpp
 *
 * @brief Implementations of the TrainSystem class
 *
 * @author Andrew Toader
 *
 * @date 10.01.2020
 *
*/

#include "TrainSystem.hpp"  // Definition of class
#include <vector>           // For accessing list of Trains, Tracks, Signals
#include "Logger.hpp"       // For logging events (debugging purposes)

/**
 * @brief	gets singleton instance
 *
 * @return 	reference to this singleton TrainSystem Object
 *
 */
TrainSystem& TrainSystem::GetInstance()
{
	static TrainSystem* pInstance = new TrainSystem();
	return *(pInstance);
}

/**
 *@brief Create(dispatch) a new train by creating
 * the Train object then adding it to the class member vector
 *
 * @param[in]	block_to
 *
 * @return pointer to newly created Train struct
 *
 */
Train* TrainSystem::CreateNewTrain(int block_to)
{
	// Set the train number to the next available
	int num = p_trains.size() + 1;

	// Create an object with that number
	Train* p_temp;
	p_temp = new Train(num, block_to);

	// Append the train to the train list
	p_trains.push_back(p_temp);
	train_numbers.push_back(num);

	// Add Speed and Authority to train
	p_temp->authority = 1000;           // feet
	p_temp->command_speed = 25;         // mph

	// return the object just created
	return p_temp;
}
