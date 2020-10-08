//
// Created by Nathan Swanson on 10.4.20
// TrackSystem Implementation file
//
#include <iostream>
#include "TrackSystem.h"
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

void update_occupancies(SW_Track& a, int occ)
{


	// Set occupied member variable as true
	a.occ_update(occ);


}






// TESTING
void TrackSystem::printout()
	{

	}
