//
// Created by Nathan Swanson on 10.4.20
// TrackSystem Implementation file
//
#include <iostream>
#include "TrackSystem.hpp"
#include <vector>

/**
 * @brief	Gets the singleton instance
 * @return	TrackSystem singleton pointer
*/
TrackSystem& TrackSystem::GetInstance()
{
	static TrackSystem* pInstance = new TrackSystem();
	return *(pInstance);
}


// Create new track
SW_Track* TrackSystem::create_new_track( int train_id,int destination,int authority, int comm_speed)
{

	// Create an object 
	SW_Track* p_temp;
	p_temp = new SW_Track(train_id, destination, authority, comm_speed);
	p_tracks.push_back(p_temp);


	// return the object just created
	return p_temp;
}

int TrackSystem::get_track_occ()
{

	// Create an object 
	int occ = p_tracks[0]->occupancy;
	
	return occ;
}

int TrackSystem::get_pos()
{

	// Create an object 
	int pos = p_tracks[0]->switch_position;
	
	return pos;
}

void TrackSystem::update_occupancies( int occ)
{


	// Set occupied member variable as true
	p_tracks[0]-> occupancy = occ;


}






// TESTING
void TrackSystem::printout()
	{

	}
