/**
 * @file CTCDef.hpp
 *
 * @brief Declaration of Structs and Enums used in CTC
 *
 * @author Andrew Toader
 *
 * @date 10.01.2020
*/

#ifndef CTC_CTCDEF_H
#define CTC_CTCDEF_H

#include <vector>
#include <string>

/**
 * @enum Line
 *
 * @brief Enumerated type telling line or train
 *
 * @li LINE_GREEN
 * @li LINE_RED
 *
 */
enum Line {LINE_GREEN, LINE_RED, LINE_UNSPEC};

/**
 *  @struct Train
 *
 * @brief Structure that holds data about a single train (id, command speed, authority, destination block)
 *
 */
struct Train
{
	int train_id;
	int command_speed;
	int authority;
	int destination_block;
	enum Line line_on;
	int index_on_route;
	std::vector<int> route_blocks;
	std::vector<int> rout_switches;

	// Constructor to initialize elements
	Train(int id, int block)
	{
		train_id = id;
		destination_block = block;
		command_speed = 0;
		authority = 0;
		line_on = LINE_UNSPEC;
		index_on_route = 0;
	}
};

/**
 * @struct Track
 *
 * @brief Structure that holds data about a single track (open, occupied)
 *
 */
struct Track
{
	bool open;
	bool occupied;

	// Constructor to intitialize elements (track open, not occupied)
	Track()
	{
		open = true;
		occupied = false;
	}
};

/**
 * @enum Color
 *
 * @brief Enumerated type telling light color
 *
 * @li LIGHT_RED
 * @li LIGHT_YELLOW
 * @li LIGHT_GREEN
 *
 */
enum Color {LIGHT_RED, LIGHT_YELLOW, LIGHT_GREEN};

/**
 * @struct Signal
 *
 * @brief Structure that holds data about a single Signal (color, track on)
 *
 */
struct Signal
{
	enum Color status;
	Track* track_on;

	// Constructor to initialize color to red
	Signal()
	{
		status = LIGHT_RED;
		track_on = nullptr;
	}
	// Destructor to release pointer
	~Signal()
	{
		delete track_on;
	}
};

/**
 * @struct Switch
 *
 * @brief Structure that holds data about a single Switch (pointing to)
 *
 * @note -1 denotes yard
 *
 */
struct Switch
{
	int less_block;
	int greater_block;
	int pointing_to;

	Switch(int less, int greater)
	{
		less_block =  less;
		greater_block = greater;
		pointing_to = less;
	}

	std::string TrackSwitchToString()
	{
		std::string to_return;

		if(pointing_to == -1)
		{
			to_return = "Yrd";
		}
		else if(pointing_to < 10)
		{
			to_return.append("00");
			to_return.append(std::to_string(pointing_to));
		}
		else if(pointing_to < 100)
		{
			to_return.append("0");
			to_return.append(std::to_string(pointing_to));
		}
		else
		{
			to_return.append(std::to_string(pointing_to));
		}
		return to_return;
	}
};

#endif //CTC_CTCDEF_H
