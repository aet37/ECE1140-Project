//
// Edited by Nathan Swanson on 11.11.20
//

#ifndef TRACK_CONTROLLER_HPP
#define TRACK_CONTROLLER_HPP
#include <vector>
#include <queue>
#include "UserProgram.hpp"

// class that holds information on a track controller
class TrackController
{
	private:
	// Variables

	//uploaded pLC program
	UserProgram PLC_Program;

	//suggested speed sent from CTC
	int suggested_speed=0;

	//vector that holds occupancies controlled by controller
	std::vector<bool> occupancy;

	//vector that holds previous occupancies controlled by controller
	std::vector<bool> prevOccupancy;

	//switch position
	bool switch_position=0;

	//queue that holds switch positions to be popped off
	std::queue<bool> positionQueue;

	//set to 1 when controller is created
	bool setup=0;

	//variable that tells controller when to pop off next value
	bool popNext=0;


	public:

	//constructor
	TrackController();
	
	//returns switch position
	bool getSwitchPos();

	//changes switch position
	bool changeSwitchPos();

	//returns occupancies of controller
	std::vector<bool> getOccupancy();

	/*bool setupOccupancy(std::vector<bool> newOccupancy)
	{
		if(newOccupancy.size()==occupancy.size()&&setup==1)
		{
			prevOccupancy=occupancy;
			occupancy=newOccupancy;
			return 1;
		}
		else if(setup==0)
		{
			occupancy=newOccupancy;
			setup=1;
		}
		else
		{
			return 0;
		}
	}*/

	//sets a block in the controller as occupied
	void setOccupied(int a);

	//sets a block in the controller as unoccupied
	void setUnoccupied(int a);

	//returns suggested speed sent by CTC
	int getSuggestedSpeed();

	//suggested speed sent by CTC
	void setSuggestedSpeed(int a);

	//used at train dispatch to put a new value on the switch
	void addToQueue(bool a);

	//sets Popnext to 1
	void setPopNext();
	
	//pops next value off controller, resets Popnext
	bool queueUpdate();

	//loops through plc program
	void loop();


	
};





#endif 
