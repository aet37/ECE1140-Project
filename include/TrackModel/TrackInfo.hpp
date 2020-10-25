/**
 * @file TrackInfo.hpp
 *
 * @brief Declaration of the TrackInfo class; will run the TrackModel module
 *
 * @author Evan Kutney
 *
 * @date 10.17.2020
*/

#include <vector>       // For list of trains, tracks, signals
#include "TrackModelDef.hpp"     // For Train, Track, Signal objects
#include "Logger.hpp"      // For Logging (debugging)

#ifndef CTC_TRAIN_SYSTEM_H
#define CTC_TRAIN_SYSTEM_H

/**
 * @class TrackInfo
 *
 * @brief Singleton class responsible for running vital operations of the CTC
 */
class TrackInfo
{
	private:
		/**
		 * @brief Private constructor for singleton object TrackInfo
		 */
		TrackInfo()
		{
			ReadInTrackLayout();
			LOG_CTC("From TrackInfo::TrackInfo() : TrackInfo Class Created");
		}

		/// List of Trains
		std::vector<int> train_numbers;

		/// List of Tracks
		std::vector<Track*> p_tracks;

	public:
		// /**
		//  * @brief	gets singleton instance
		//  *
		//  * @return 	reference to this singleton TrackInfo Object
		//  *
		//  */
		// static std::vector<Track> InitializeSystem();

		/**
		* @brief Read in the layout of the track and add it to the list of tracks.
        * Also create a list of possible paths that can be taken on this track
		* @param int trackNumber
		*
		* @return bool trackObtained
		*
		*/
		void getTrack(int trackNumber);


        /**
		* @brief Gets the track object based on the track number input
		* @param std::string line, std::vector<Station> stations, std::vector<Switch> switches, int totalBlocks, std::vector<Block> blockList
		*
		* @return none
		*
		*/
		void AddTrackLayout(std::string line, /*std::vector<Station> stations, std::vector<Switch> switches,*/ int totalBlocks, std::vector<Block> blockList);

		/**
		* @brief Get the Array of track pointers
		 *
		* @param none
		*
		* @return std::vector<Track*>
		*
		*/
		std::vector<Track*> GetTrackArr();

		/**
		* @brief Get the Array of train pointers
		*
		* @param none
		*
		* @return vector<Train*>
		*
		*/
		std::vector<Train*> GetTrainArr();

};

#endif //CTC_TRAIN_SYSTEM_H