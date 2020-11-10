//
// Created by Nathan Swanson on on 10.6.20.
// System which will run the SW Track Controller module
//
#ifndef SW_TRACK_SYSTEM_HPP
#define SW_TRACK_SYSTEM_HPP

#include <vector>
#include "SWTrackDef.hpp"

class TrackSystem
{
	private:
		/**
		 * @brief constructor for singleton object TrackSystem
		 */
		TrackSystem()
		{ }

		// Tracks
		std::vector<int> switch_numbers;
		std::vector<SW_Track*> p_tracks;
        std::vector<int> track_occupancies;

	

	public:
		/**
		 * @brief	gets singleton instance
		 * @return 	reference to this singleton TrackSystem Object
		 */
		static TrackSystem& GetInstance();
		


		//create a new track with inputted variables
		SW_Track* create_new_track(int ,int , int,int );

		// update the occupancy of a single track
		void update_occupancies(int );

		
	int get_track_occ();

	int get_pos();
		

		// TESTING PURPOSES
		void printout();
};

#endif // SW_TRACK_SYSTEM_HPP
