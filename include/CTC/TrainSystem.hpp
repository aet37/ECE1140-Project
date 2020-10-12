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
#include "Logger.hpp"      // For Logging (debugging)

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
		{
			ImportTrackLayout();
			LOG_CTC("From TrainSystem::TrainSystem() : TrainSystem Class Created");
		}

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
		* @brief Import the layout of the track
		 *
		* @param none
		*
		* @return None
		*
		*/
		void ImportTrackLayout();

		/**
		* @brief Get the Array of track pointers
		 *
		* @param none
		*
		* @return vector<Track*>
		*
		*/
		std::vector<Track*> GetTrackArr();

		/**
		 * @brief Create(dispatch) a new train by creating
		 * the Train object then adding it to the class member vector
		 *
		 * @param[in]	block_to
		 *
		 * @return pointer to newly created Train struct
		 *
		 */
		Train* CreateNewTrain(int block_to);

		/**
		* @brief change Track status to occupied
		*
		* @param[in]	track_num
		*
		* @return none
		*
		*/
		void SetTrackOccupied(int track_num);

		/**
		* @brief change Track status to not occupied
		*
		* @param[in]	track_num
		*
		* @return none
		*
		*/
		void SetTrackNotOccupied(int track_num);
};

#endif //CTC_TRAIN_SYSTEM_H
