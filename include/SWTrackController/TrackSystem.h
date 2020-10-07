//
// Created by Nathan Swanson on on 10.6.20.
// System which will run the SW Track Controller module
//

#include <vector>
#include "SWTrackDef.h"
#include "SwitchDef.h"
#ifndef SW_TRACK_SYSTEM_H
#define SW_TRACK_SYSTEM_H

class TrackSystem
{
	private:
		/**
		 * @brief constructor for singleton object TrainSystem
		 */
		TrackSystem()
		{ }

		// Tracks
		std::vector<int> switch_numbers;
		std::vector<Switch*> p_switches;
        std::vector<int> track_occupancies;

	

	public:
		/**
		 * @brief	gets singleton instance
		 * @return 	reference to this singleton TrainSystem Object
		 */
		static TrackSystem& GetInstance();


		/**
		 *
		 * @param block_to
		 * @return pointer to Train struct
		 */
		Track* create_new_switch(int authority, int train_id, int comm_speed,int destination);

		// Send train id, authority and speed to Track Controller
		void send_track_info_ctc(Track* to_send_ctc);

        void send_track_info_tm(Track* to_send_tm);

		// TESTING PURPOSES
		void printout();
};

#endif SW_TRACK_SYSTEM_H
