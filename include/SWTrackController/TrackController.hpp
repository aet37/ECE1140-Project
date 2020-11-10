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
	
	bool getSwitchPos()
	{
		return switch_position;
	}

	bool changeSwitchPos()
	{
		if(switch_position==0)
		{
			switch_position=1;
			return switch_position;
		}
		else if(switch_position==1)
		{
			switch_position=0;
			return switch_position;
		}
	}

	std::vector<bool> getOccupancy()
	{
		return occupancy;
	}

	bool setOccupancy(std::vector<bool> newOccupancy)
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
	}

	int getSuggestedSpeed()
	{
		return suggested_speed;
	}

	void setSuggestedSpeed(int a)
	{
		suggested_speed=a;
	}

	void addToQueue(bool a)
	{
		positionQueue.push(a);
	}

	void setPopNext()
	{
		popNext=1;
	}
	
	bool queueUpdate()
	{
		if(popNext=1)
		{
			positionQueue.pop();
			switch_position=positionQueue.front();
			popNext=0;
			
		}
		
	}

	void loop()
	{
		PLC_Program();
		queueUpdate();




	}


	
};





#endif 
