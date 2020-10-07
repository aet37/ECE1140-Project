//
// Created by Nathan Swanson on 10.6.20
//

#ifndef SW_TRACK_DEF_H
#define SW_TRACK_DEF_H

// Structure that holds data about a single train
struct Track
{
	// Variables
	int train_id;
	int command_speed;
	int authority;
	int destination_block;
	int occupancies;

	// Constructor to initialize elements
	Track()
	{
		train_id = 0;
		destination_block = 0;
		command_speed = 0;
		authority = 0;
		occupancies = 0;
	}
	
};

struct Switch
{

	bool switch_position;
	int switch_id;



		Switch()
		{
			switch_position = 0;
			
		}



};







#endif //SW_TRACK_DEF_H
