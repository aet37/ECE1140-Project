#include "TrackController.hpp"
#include <Logger.hpp>
#include <iostream>

	//constructor
    TrackController::TrackController()
    {
		occupancy.clear();
		
    }

	//retuns switch position
    bool TrackController::getSwitchPos()
	{
		return switch_position;
	}

	//changes switch position
	bool TrackController::changeSwitchPos()
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

	//returns occupancy vector
	std::vector<bool> TrackController::getOccupancy()
	{
		
		return occupancy;
	}

	void TrackController::setupOccupancy(std::vector<bool> newOccupancy)
	{
		
		for(int i=0;i<newOccupancy.size();i++)
		{

			occupancy.push_back(newOccupancy[i]);

		}
	}

	//sets specified block as occupied 
	void TrackController::setOccupied(int a)
	{
		prevOccupancy = occupancy;

		occupancy[a] = 1;
	}

	//sets specified block as unoccupied
	void TrackController::setUnoccupied(int a)
	{

		prevOccupancy = occupancy;

		occupancy[a] = 0;
	}

	//returns suggested speed
	int TrackController::getSuggestedSpeed()
	{
		return suggested_speed;
	}

	//sets suggested speed
	void TrackController::setSuggestedSpeed(int a)
	{
		suggested_speed=a;
	}

	//adds a bool to the queue
	void TrackController::addToQueue(bool a)
	{
		positionQueue.push(a);
	}

	//sets value to pop next
	void TrackController::setPopNext()
	{
		popNext=1;
	}
	
	//pops next, resets popnext
	bool TrackController::queueUpdate()
	{
		if(popNext=1)
		{
			positionQueue.pop();
			switch_position=positionQueue.front();
			popNext=0;
			
		}
		
	}

	//program that loops plc
	void TrackController::loop()
	{
		//PLC_Program();
		queueUpdate();
	}

