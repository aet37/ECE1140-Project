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

	// Constructor to initialize elements
	Train(int id, int block)
	{
		train_id = id;
		destination_block = block;
		command_speed = 0;
		authority = 0;
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

#endif //CTC_CTCDEF_H
