//
// Created by Andrew Toader on 10.1.20.
// System which will run the CTC module
//

#include <vector>
#include "CTCDef.h"

#ifndef CTC_TRAIN_SYSTEM_H
#define CTC_TRAIN_SYSTEM_H

class TrainSystem
{
	private:
		/**
		 * @brief constructor for singleton object TrainSystem
		 */
		TrainSystem()
		{ }

		// Trains
		std::vector<int> train_numbers;
		std::vector<Train*> p_trains;

		// Tracks
		std::vector<Track*> p_tracks;

		// Signals
		std::vector<Signal*> p_signals;

	public:
		/**
		 * @brief	gets singleton instance
		 * @return 	reference to this singleton TrainSystem Object
		 */
		static TrainSystem& GetInstance();

		// Import track from Track Model
		void import_track_from_tm();

		/**
		 *
		 * @param block_to
		 * @return pointer to Train struct
		 */
		Train* create_new_train(int block_to);

		// Send train id, authority and speed to Track Controller
		void send_train_info_tc(Train* to_send);

		// TESTING PURPOSES
		void printout();
};

#endif //CTC_TRAIN_SYSTEM_H
