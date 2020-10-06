//
// Created by Andrew Toader on 10.1.20.
// TrainSystem Implementation file
//
#include <iostream>
#include "../../include/CTC/TrainSystem.h"
#include <vector>

/**
 * @brief	Gets the singleton instance
 * @return	TrainSystem singleton pointer
*/
TrainSystem& TrainSystem::GetInstance()
{
	static TrainSystem* pInstance = new TrainSystem();
	return *(pInstance);
}

// Import track from Track Model
void TrainSystem::import_track_from_tm()
{

}

// Create new train
Train* TrainSystem::create_new_train(int block_to)
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

// Send train id, authority and speed to Track Controller
void TrainSystem::send_train_info_tc(Train* to_send)
{

}

// TESTING
void TrainSystem::printout()
{
	std::cout << "Size (Trains): " << p_trains.size() << std::endl;
	if(p_trains.size() > 0)
	{
		std::cout << p_trains[0]->command_speed << std::endl;
		std::cout << p_trains[0]->authority << std::endl;
		std::cout << p_trains[0]->train_id << std::endl;
	}
}