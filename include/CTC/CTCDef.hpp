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

#include <map>

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
	int block_on;

	// Constructor to initialize elements
	Train(int id, int block)
	{
		train_id = id;
		destination_block = block;
		command_speed = 0;
		authority = 0;
		line_on = LINE_UNSPEC;
		block_on = -1;
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
};

std::string SwitchToString(int sw)
{
	std::string to_return;

	if(sw == -1)
	{
		to_return = "Yrd";
	}
	else if(sw < 10)
	{
		to_return.append("00");
		to_return.append(std::to_string(sw));
	}
	else if(sw < 100)
	{
		to_return.append("0");
		to_return.append(std::to_string(sw));
	}
	else
	{
		to_return.append(std::to_string(sw));
	}
	return to_return;
}

#endif //CTC_CTCDEF_H
