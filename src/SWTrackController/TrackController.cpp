#include "TrackController.hpp"
	
    TrackController::TrackController()
    {
        

    }
    
    bool TrackController::getSwitchPos()
	{
		return switch_position;
	}

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

	std::vector<bool> TrackController::getOccupancy()
	{
		return occupancy;
	}

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

	void TrackController::setOccupied(int a)
	{
		prevOccupancy = occupancy;

		occupancy[a] = 1;
	}

	void TrackController::setUnoccupied(int a)
	{
		prevOccupancy = occupancy;

		occupancy[a] = 0;
	}



	int TrackController::getSuggestedSpeed()
	{
		return suggested_speed;
	}

	void TrackController::setSuggestedSpeed(int a)
	{
		suggested_speed=a;
	}

	void TrackController::addToQueue(bool a)
	{
		positionQueue.push(a);
	}

	void TrackController::setPopNext()
	{
		popNext=1;
	}
	
	bool TrackController::queueUpdate()
	{
		if(popNext=1)
		{
			positionQueue.pop();
			switch_position=positionQueue.front();
			popNext=0;
			
		}
		
	}

	void TrackController::loop()
	{
		//PLC_Program();
		queueUpdate();




	}

