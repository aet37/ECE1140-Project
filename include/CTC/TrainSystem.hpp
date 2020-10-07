/**
 * @file TrainSystem.hpp
 *
 * @brief Declaration of the TrainSystem class; will run the CTC module
 *
 * @author Andrew Toader
 *
 * @date 10.01.2020
*/

#include <vector>       // For list of trains, tracks, signals
#include "CTCDef.hpp"     // For Train, Track, Signal objects

#ifndef CTC_TRAIN_SYSTEM_H
#define CTC_TRAIN_SYSTEM_H

/**
 * @class TrainSystem
 *
 * @brief Singleton class responsible for running vital operations of the CTC
 */
class TrainSystem
{
	private:
		/**
		 * @brief Private constructor for singleton object TrainSystem
		 */
		TrainSystem()
		{ }

		/// List of Trains
		std::vector<int> train_numbers;

		/// List of Train Numbers used
		std::vector<Train*> p_trains;

		/// List of Tracks
		std::vector<Track*> p_tracks;

		/// List of Signals
		std::vector<Signal*> p_signals;

	public:
		/**
		 * @brief	gets singleton instance
		 *
		 * @return 	reference to this singleton TrainSystem Object
		 *
		 */
		static TrainSystem& GetInstance();

		/**
		 *@brief Create(dispatch) a new train by creating
		 * the Train object then adding it to the class member vector
		 *
		 * @param[in]	block_to
		 *
		 * @return pointer to newly created Train struct
		 *
		 */
		Train* CreateNewTrain(int block_to);
};

#endif //CTC_TRAIN_SYSTEM_H
