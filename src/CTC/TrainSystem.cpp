//
// Created by Andrew Toader on 10.1.20.
// TrainSystem Implementation file
//
#include <iostream>
#include "../../include/CTC/TrainSystem.h"
#include <vector>

// Constructor
TrainSystem::TrainSystem()
{

}

// Destructor
TrainSystem::~TrainSystem()
{
	Train* to_delete1 = nullptr;
	// Free all of the pointers
	while(p_trains.size() != 0)
	{
		to_delete1 = p_trains[p_trains.size() - 1];
		delete to_delete1;
		p_trains.pop_back();
	}
	Track* to_delete2 = nullptr;
	while(p_tracks.size() != 0)
	{
		to_delete2 = p_tracks[p_tracks.size() - 1];
		delete to_delete2;
		p_tracks.pop_back();
	}
	Signal* to_delete3 = nullptr;
	while(p_signals.size() != 0)
	{
		to_delete3 = p_signals[p_signals.size() - 1];
		delete to_delete3;
		p_signals.pop_back();
	}
}

// Import track from Track Model
void TrainSystem::import_track_from_tm()
{

}

// Create new train
void TrainSystem::create_new_train(enum Line line_to_add)
{
	// Set the train number to the next available
	int num = p_trains.size() + 1;

	// Create an object with that number
	Train* p_temp;
	p_temp = new Train(num, line_to_add);

	// Append the train to the train list
	p_trains.push_back(p_temp);
	train_numbers.push_back(num);

	// Add Speed and Authority to train
	p_temp->authority = 1000;           // feet
	p_temp->command_speed = 25;         // mph

	// Send the train info to Track Controller
	send_train_info_tc(p_temp);

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
		std::cout << p_trains[0]->line_on << std::endl;
		std::cout << p_trains[0]->train_id << std::endl;
	}
}