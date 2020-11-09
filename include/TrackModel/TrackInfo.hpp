/**
 * @file TrackInfo.hpp
 *
 * @brief Declaration of the TrackInfo class; will run the TrackModel module
 *
 * @author Evan Kutney
 *
 * @date 10.17.2020
*/
#ifndef TRACK_INFO_HPP
#define TRACK_INFO_HPP

#include <vector>       // For list of trains, tracks, signals
#include "TrackModelDef.hpp"     // For Train, Track, Signal objects
#include "Logger.hpp"      // For Logging (debugging)


namespace TrackModel
{

// FORWARD DECLARATIONS
class Track;

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
			LOG_TRACK_MODEL("TrackInfo Class Created");
		}

		/// List of Trains
		std::vector<int> train_numbers;

		/// List of Tracks
		std::vector<Track*> m_pTrackList;

	public:
		/**
		 * @brief	gets singleton instance
		 *
		 * @return 	reference to this singleton TrackInfo Object
		 *
		 */
		static TrackInfo& GetInstance()
		{
			static TrackInfo* pInstance = new TrackInfo();
			return *(pInstance);
		}

		/**
		* @brief Read in the layout of the track and add it to the list of tracks.
        * Also create a list of possible paths that can be taken on this track
		* @param int trackNumber
		*
		* @return bool trackObtained
		*
		*/
		Track* getTrack(int trackNumber);


        /**
		* @brief Gets the track object based on the track number input
		* @param std::string line, std::vector<Station> stations, std::vector<Switch> switches, int totalBlocks, std::vector<Block> blockList
		*
		* @return none
		*
		*/
		void AddTrackLayout(std::string line, int number, int totalBlocks);
};

} // namespace TrackModel

#endif // TRACK_INFO_HPP