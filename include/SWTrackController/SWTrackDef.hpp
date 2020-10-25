//
// Created by Nathan Swanson on 10.6.20
//

#ifndef SW_TRACK_DEF_HPP
#define SW_TRACK_DEF_HPP

// Structure that holds data about a single track
struct SW_Track
{
	// Variables
	int train_id;
	int command_speed;
	int authority;
	int destination_block;
	int occupancy;
	int switch_position;

	
	SW_Track(int id, int destination, int auth, int speed)
	{
		train_id = id;
		destination_block = destination;
		command_speed = speed;
		authority = auth;
		occupancy = 0;
		if(destination ==15)
		{
			switch_position = 11;
		}
		else
		{
			switch_position =6;
		}

	}	
	void occ_update(int occ)
	{
		occupancy = occ;

	}
};





#endif //SW_TRACK_DEF_HPP
