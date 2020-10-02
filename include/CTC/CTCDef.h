//
// Created by Andrew Toader on 10.1.20.
//

#ifndef CTC_CTCDEF_H
#define CTC_CTCDEF_H

// enumerated definition for the line the train is on
enum Line {LINE_BLUE, LINE_GREEN};

// Structure that holds data about a single train
struct Train
{
	// Variables
	int train_id;
	int command_speed;
	int authority;
	enum Line line_on;

	// Constructor to initialize elements
	Train(int id, enum Line on)
	{
		train_id = id;
		line_on = on;
		command_speed = 0;
		authority = 0;
	}
};

// Structure that holds data about a single train
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

// Enumerated type telling light color
enum Color {LIGHT_RED, LIGHT_YELLOW, LIGHT_GREEN};

// Structure that holds data about a single Signal
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
