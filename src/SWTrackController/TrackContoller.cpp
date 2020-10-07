//
// Created by Nathan Swanson on 10.4.20
// TrackSystem Implementation file
//
#include <iostream>
#include "../../include/SWTrackController/TrackSystem.h"
#include <vector>

/**
 * @brief	Gets the singleton instance
 * @return	TrainSystem singleton pointer
*/
TrackSystem& TrackSystem::GetInstance()
{
	static TrackSystem* pInstance = new TrackSystem();
	return *(pInstance);
}


// Create new train
Track* TrackSystem::create_new_switch(int authority, int train_id, int comm_speed,int destination)
{
	// Set the train number to the next available
	int num = p_switches.size() + 1;

	// Create an object with that number
	Switch* p_temp;
	p_temp = new Switch(num, block_to);

	// Append the train to the train list
	p_switches.push_back(p_temp);
	switch_numbers.push_back(num);

	// Add Speed and Authority to train
	p_temp->authority = 1000;           // feet
	p_temp->command_speed = 25;         // mph

	// return the object just created
	return p_temp;
}

// Send train id, authority and speed to Track Controller
void TrackSystem::send_track_info_ctc(Track* to_send_ctc)
{

}

void TrackSystem::send_track_info_tm(Track* to_send_tm)
{

}

// TESTING
void TrackSystem::printout()
{
	std::cout << "Size (Trains): " << p_switches.size() << std::endl;
	if(p_switches.size() > 0)
	{
		std::cout << p_tracks[0]->command_speed << std::endl;
		std::cout << p_tracks[0]->authority << std::endl;
		std::cout << p_tracks[0]->train_id << std::endl;
	}
}