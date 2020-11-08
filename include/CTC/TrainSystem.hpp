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

			// Create routes
			green_route_blocks = {-1, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84, 83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 , 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, -1};
			green_route_switches = {0, 0, 0, 1, 1, 1, 0, 1, 0, 0};

			red_route_blocks = {-1, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75, 74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 1, 2, 3, 4, 5, 6, 7, 8, -1};
			red_route_switches = {0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1};


			LOG_CTC("From TrainSystem::TrainSystem() : TrainSystem Class Created");
		}

		/// List of Trains
		std::vector<int> train_numbers;

		/// List of Train Numbers used
		std::vector<Train*> p_trains;

		/// List of Tracks
		std::vector<Track*> p_blocks_red;
		std::vector<Track*> p_blocks_green;

		/// List of Signals
		std::vector<Signal*> p_signals;

		/// List of Switches
		std::vector<Switch*> p_switches_green;
		std::vector<Switch*> p_switches_red;

	public:
		/// Green line Route in Blocks
		std::vector<int> green_route_blocks;

		/// Green line Route in Switches
		std::vector<int> green_route_switches;

		/// Red line Route in Blocks
		std::vector<int> red_route_blocks;

		/// Red line Route in Switches
		std::vector<int> red_route_switches;

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
		* @param Line
		*
		* @return vector<Track*>
		*
		*/
		std::vector<Track*> GetTrackArr(enum Line ln);

		/**
		* @brief Get the Array of Signal pointers
		*
		* @param Line
		*
		* @return vector<Signal*>
		*
		*/
		std::vector<Switch*> GetSwitchesArr(enum Line ln);

		/**
		* @brief Get the Array of train pointers
		*
		* @param none
		*
		* @return vector<Train*>
		*
		*/
		std::vector<Train*> GetTrainArr();

		/**
		 * @brief Create(dispatch) a new train by creating
		 * the Train object then adding it to the class member vector
		 *
		 * @param[in]	block_to
		 *
		 * @return pointer to newly created Train struct
		 *
		 */
		Train* CreateNewTrain(int block_to, enum Line ln);

		/**
		* @brief change Track status to occupied
		*
		* @param[in]	track_num
		*
		* @return none
		*
		*/
		void SetTrackOccupied(int track_num, enum Line ln);

		/**
		* @brief change Track status to not occupied
		*
		* @param[in]	track_num
		*
		* @return none
		*
		*/
		void SetTrackNotOccupied(int track_num, enum Line ln);

		/**
		 * @brief change Track status to occupied
		 *
		 * @param[in]	switch_num, Line, update_pos
		 *
		 * @return none
		 *
		*/
		void SetSwitch(int switch_num, enum Line ln, int pos);

		/**
		 * @brief update the train position (to be called every time occupancy is changed)
		 *
		 * @param[post] train location for each Train* in p_trains updated with current location
		 *
		 * @return none
		 *
		*/
		void UpdateTrainPosition();
};

#endif //CTC_TRAIN_SYSTEM_H