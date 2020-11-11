//
// Created by Nathan Swanson on 10.6.20
//

#ifndef TRACK_CONTROLLER_HPP
#define TRACK_CONTROLLER_HPP
#include <UserProgram.hpp>
#include <vector>
#include <queue>

// class that holds information on a track controller
class TrackController
{
	private:
	// Variables
	UserProgram PLC_Program;
	int suggested_speed=0;
	std::vector<bool> occupancy;
	std::vector<bool> prevOccupancy;
	bool switch_position=0;
	std::queue<bool> positionQueue;
	bool setup=0;
	bool popNext=0;


	public:

	TrackController();
	
	bool getSwitchPos();

	bool changeSwitchPos();

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

	void setOccupied(int a);

	void setUnoccupied(int a);



	int getSuggestedSpeed();

	void setSuggestedSpeed(int a);

	void addToQueue(bool a);

	void setPopNext();
	
	bool queueUpdate();

	void loop();


	
};





#endif 
