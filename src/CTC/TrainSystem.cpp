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

	// Log that a track is occupied
	LOG_CTC("From TrainSystem::SetTrackOccupied() : Track %d is occupied", track_num);
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
	// Log that a track is occupied
	LOG_CTC("From TrainSystem::SetTrackNotOccupied() : Track %d is NOT occupied", track_num);
}