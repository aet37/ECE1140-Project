/**
 * @file TrainSystem.cpp
 *
 * @brief Implementations of the TrainSystem class
 *
 * @author Andrew Toader
 *
 * @date 10.01.2020
 *
*/

#include "TrainSystem.hpp"  // Definition of class
#include <vector>           // For accessing list of Trains, Tracks, Signals
#include "Logger.hpp"       // For logging events (debugging purposes)
#include "CTCMain.hpp"
#include "SWTrackControllerMain.hpp"    // For sending information to the Train Controller

/**
 * @brief	gets singleton instance
 *
 * @return 	reference to this singleton TrainSystem Object
 *
 */
TrainSystem& TrainSystem::GetInstance()
{
	static TrainSystem* pInstance = new TrainSystem();
	return *(pInstance);
}

/**
* @brief Import the layout of the track
 *
* @param none
*
* @return None
*
*/
void TrainSystem::ImportTrackLayout()
{
	// Initialize the red track blocks
	Track* ptemp_track = nullptr;
	for(int i = 0; i < 76; i++)
	{
		ptemp_track = new Track();
		p_blocks_red.push_back(ptemp_track);
	}

	// Initialize the green track blocks
	for(int i = 0; i < 150; i++)
	{
		ptemp_track = new Track();
		p_blocks_green.push_back(ptemp_track);
	}
	ptemp_track = nullptr;

	// Create Green Switches
	Switch* sw1 = new Switch(1, 12);
	Switch* sw2 = new Switch(30, 150);
	Switch* sw3 = new Switch(-1, 59);
	Switch* sw4 = new Switch(-1, 61);
	Switch* sw5 = new Switch(76, 101);
	Switch* sw6 = new Switch(86, 100);
	p_switches_green.push_back(sw1);
	p_switches_green.push_back(sw2);
	p_switches_green.push_back(sw3);
	p_switches_green.push_back(sw4);
	p_switches_green.push_back(sw5);
	p_switches_green.push_back(sw6);

	// Create Red Switches
	Switch* rsw1 = new Switch(-1, 8);
	Switch* rsw2 = new Switch(1, 15);
	Switch* rsw3 = new Switch(28, 76);
	Switch* rsw4 = new Switch(32, 72);
	Switch* rsw5 = new Switch(39, 71);
	Switch* rsw6 = new Switch(43, 67);
	Switch* rsw7 = new Switch(53, 66);
	p_switches_red.push_back(rsw1);
	p_switches_red.push_back(rsw2);
	p_switches_red.push_back(rsw3);
	p_switches_red.push_back(rsw4);
	p_switches_red.push_back(rsw5);
	p_switches_red.push_back(rsw6);
	p_switches_red.push_back(rsw7);

	LOG_CTC("From TrainSystem::ImportTrackLayout() : Tracks Created");
}

/**
* @brief Get the Array of track pointers for the green track
 *
* @param[in] enum Line
*
* @return vector<Track*>
* @return Throw Error if incorrect line is specified
*
*/
std::vector<Track*> TrainSystem::GetTrackArr(enum Line ln)
{
	if(ln == LINE_GREEN)
	{
		return p_blocks_green;
	}
	else if(ln == LINE_RED)
	{
		return p_blocks_red;
	}
	else
	{
		throw std::logic_error("TrainSystem::GetTrackArr : Invalid Line Argument");
	}
}

/**
* @brief Get the Array of Signal pointers
*
* @param Line
*
* @return vector<Signal*>
*
*/
std::vector<Switch*> TrainSystem::GetSwitchesArr(enum Line ln)
{
	if(ln == LINE_GREEN)
	{
		return p_switches_green;
	}
	else if(ln == LINE_RED)
	{
		return p_switches_red;
	}
	else
	{
		throw std::logic_error("TrainSystem::GetTrackArr : Invalid Line Argument");
	}
}

/**
* @brief Get the Array of train pointers
*
* @param none
*
* @return vector<Train*>
*
*/
std::vector<Train*> TrainSystem::GetTrainArr()
{
	return p_trains;
}

/**
 *@brief Create(dispatch) a new train by creating
 * the Train object then adding it to the class member vector
 *
 * @param[in]	block_to
 *
 * @return pointer to newly created Train struct
 *
 */
Train* TrainSystem::CreateNewTrain(int block_to, enum Line ln)
{
	// Set the train number to the next available
	int num = p_trains.size() + 1;

	// Create an object with that number
	Train* p_temp;
	p_temp = new Train(num, block_to);

	// Append the train to the train list
	p_trains.push_back(p_temp);
	train_numbers.push_back(num);

	// Add Speed and Authority to train
	p_temp->authority = 1000;           // m
	p_temp->command_speed = 40;         // km/hr

	// Log creation of object
	LOG_CTC("From TrainSystem::CreateNewTrain : Created Train #%d", p_temp->train_id);

	// return the object just created
	return p_temp;
}

/**
* @brief change Track status to occupied
*
* @param[in]	track_num
* @param[in]	Line
*
* @return Throw Error if track is out of range or invalid line entered
*
*/
void TrainSystem::SetTrackOccupied(int track_num, enum Line ln)
{
	if(ln == LINE_GREEN)
	{
		// Make sure track is not out of range
		if ((track_num < 1) || track_num > p_blocks_green.size())
		{
			throw std::logic_error("TrainSystem::SetTrackOccupied() index out of bounds");
		}

		// Set occupied member variable as true
		p_blocks_green[track_num - 1]->occupied = true;
	}
	else if(ln == LINE_RED)
	{
		// Make sure track is not out of range
		if ((track_num < 1) || track_num > p_blocks_red.size())
		{
			throw std::logic_error("TrainSystem::SetTrackOccupied() : index out of bounds");
		}

		// Set occupied member variable as true
		p_blocks_red[track_num - 1]->occupied = true;
	}
	else
	{
		throw std::logic_error("TrainSystem::SetTrackOccupied() : Invalid input for Line");
	}
}

/**
* @brief change Track status to not occupied
*
* @param[in]	track_num
* @param[in]	Line
*
* @return Throw Error if track is out of range or invalid line entered
*
*/
void TrainSystem::SetTrackNotOccupied(int track_num, enum Line ln)
{
	if(ln == LINE_GREEN)
	{
		// Make sure track is not out of range
		if ((track_num < 1) || track_num > p_blocks_green.size())
		{
			throw std::logic_error("TrainSystem::SetTrackNotOccupied() index out of bounds");
		}

		// Set occupied member variable as true
		p_blocks_green[track_num - 1]->occupied = false;
	}
	else if(ln == LINE_RED)
	{
		// Make sure track is not out of range
		if ((track_num < 1) || track_num > p_blocks_red.size())
		{
			throw std::logic_error("TrainSystem::SetTrackNotOccupied() : index out of bounds");
		}

		// Set occupied member variable as true
		p_blocks_red[track_num - 1]->occupied = false;
	}
	else
	{
		throw std::logic_error("TrainSystem::SetTrackNotOccupied() : Invalid input for Line");
	}
}

/**
 * @brief change Track status to occupied
 *
 * @param[in]	switch_num, Line, update_pos
 *
 * @return none
 *
*/
void TrainSystem::SetSwitch(int switch_num, enum Line ln, int pos)
{
	if(ln == LINE_GREEN)
	{
		if(pos == 1)
		{
			p_switches_green[switch_num - 1]->pointing_to = p_switches_green[switch_num - 1]->greater_block;
		}
		else if(pos == 0)
		{
			p_switches_green[switch_num - 1]->pointing_to = p_switches_green[switch_num - 1]->less_block;
		}
		else
		{
			throw std::logic_error("TrainSystem::SetSwitch : Invalid position given (not 1 or 0)");
		}
	}
	if(ln == LINE_RED)
	{
		if(pos == 1)
		{
			p_switches_red[switch_num - 1]->pointing_to = p_switches_red[switch_num - 1]->greater_block;
		}
		else if(pos == 0)
		{
			p_switches_red[switch_num - 1]->pointing_to = p_switches_red[switch_num - 1]->less_block;
		}
		else
		{
			throw std::logic_error("TrainSystem::SetSwitch : Invalid position given (not 1 or 0)");
		}
	}
	else
	{
		throw std::logic_error("TrainSystem::SetSwitch : Invalid Line provided");
	}
}

/**
 * @brief update the train position (to be called every time occupancy is changed)
 *
 * @param[post] train location for each Train* in p_trains updated with current location
 *
 * @return none
 *
*/
void TrainSystem::UpdateTrainPosition()
{
	for(int i = 0; i < p_trains.size(); i++)
	{
		if(p_trains[i]->line_on == LINE_GREEN)      // If train is on GREEN Line
		{
			if(p_trains[i]->index_on_route == 0)        // Has not made it out of the yard yet
			{
				if(p_blocks_green[green_route_blocks[1] - 1]->occupied == false)
				{
					p_trains[i]->index_on_route++;
					p_trains[i]->authority--;
				}
				else
				{
					continue;
				}
			}
			else if(p_trains[i]->index_on_route == (green_route_blocks.size() - 1))     // Reached the yard (end)
			{
				// Free the train and delete it from the vector
				delete p_trains[i];
				p_trains.erase(p_trains.begin() + i);
				i--;
				continue;
			}
			else
			{
				if(p_blocks_green[p_trains[i]->index_on_route - 1]->occupied == false)
				{
					p_trains[i]->index_on_route++;
					p_trains[i]->authority--;
				}
				else
				{
					continue;
				}
			}
		}
		else        // If on RED Line
		{
			if (p_trains[i]->index_on_route == 0)        // Has not made it out of the yard yet
			{
				if (p_blocks_red[red_route_blocks[1] - 1]->occupied == false)
				{
					p_trains[i]->index_on_route++;
					p_trains[i]->authority--;
				}
				else
				{
					continue;
				}
			}
			else if (p_trains[i]->index_on_route == (red_route_blocks.size() - 1))     // Reached the yard (end)
			{
				// Free the train and delete it from the vector
				delete p_trains[i];
				p_trains.erase(p_trains.begin() + i);
				i--;
				continue;
			}
			else
			{
				if (p_blocks_red[p_trains[i]->index_on_route - 1]->occupied == false)
				{
					p_trains[i]->index_on_route++;
					p_trains[i]->authority--;
				}
				else
				{
					continue;
				}
			}
		}

		// Update Authority if needed
		if(p_trains[i]->authority <= 1)
		{
			// Update internal variables
			p_trains[i]->authority = 3;

			// Send to Track Controller
			Common::Request reqSend;
			reqSend.SetRequestCode(Common::RequestCode::SWTRACK_UPDATE_AUTHORITY);
			reqSend.SetData(std::to_string(i));
			reqSend.SetData(std::to_string(3));
			SWTrackController::serviceQueue.Push(reqSend);  // Push request to SW Track Controller Queue

			LOG_CTC("Authority for train %d updated and sent to SWTC", i + 1);
		}
	}
}