/**
 * @file TrackModelRequestManager.cpp
 *
 * @brief Implementation of RequestManager class for Track Model Module
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cout

// C++ PROJECT INCLUDES
#include "TrackModelRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp"   // For logging (debugging)
#include "TrainSystem.hpp"  // For handling requests
#include "TrackModelMain.hpp"  // For acessing Service Queue
#include "TrackInfo.hpp" // for getting track values
#include "Track.hpp"
#include "Block.hpp"
#include "Station.hpp"
#include "Switch.hpp"

namespace TrackModel
{

int count = 0;
// FOR GUI STUFF
void TrackModelRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
		case Common::RequestCode::TRACK_MODEL_GUI_GATHER_DATA:
		{
			//TrackModel::serviceQueue.Push(rRequest);
			std::string test = rRequest.GetData();
            int pos = test.find(' ');
            int trackNumber = std::stoi(test.substr(0, pos));

            test.erase(0, pos + 1);
            int blockNumber = std::stoi(test);

            rResponse.SetData("");

            Track *theTrack = TrackInfo::GetInstance().getTrack(trackNumber);

            std::string lineName = theTrack->getLineName();

            rResponse.AppendData(lineName);

            rResponse.AppendData(std::to_string(blockNumber));

            Block theBlock = theTrack->getBlock(blockNumber);

			rResponse.AppendData(theBlock.getSection());

            rResponse.AppendData(std::to_string(theBlock.getBlockElevation()));

            rResponse.AppendData(std::to_string(theBlock.getBlockCumulativeElevation()));

            rResponse.AppendData(std::to_string(theBlock.getBlockLength()));

            rResponse.AppendData(std::to_string(theBlock.getBlockGrade()));

            rResponse.AppendData(std::to_string(theBlock.getBlockSpeedLimit()));

            rResponse.AppendData(theBlock.getBlockUnderground());

            //station ones

            std::string stationName = theBlock.getStationName();

            if (stationName == ""){
                rResponse.AppendData("NA");
                //tickets sold
                rResponse.AppendData(std::to_string(0));
                //boarded
                rResponse.AppendData(std::to_string(0));
                // exited
                rResponse.AppendData(std::to_string(0));
                rResponse.AppendData("NA");
            }
            else
            {
				//stationName.replace(stationName.begin(), stationName.end(), ' ', '_');
				std::string tempStationName = stationName;
				if (stationName.find(' ') != std::string::npos){
					pos = stationName.find(' ');
					std::string stationName2 = stationName.substr(0, pos);
					tempStationName.erase(0, pos + 1);
					stationName = stationName2.append("_").append(tempStationName);
				}


				rResponse.AppendData(stationName);
                rResponse.AppendData(std::to_string(theBlock.getStationTicketsSold()));
                rResponse.AppendData(std::to_string(theBlock.getStationPassengersBoarded()));
                rResponse.AppendData(std::to_string(theBlock.getStationPassengersExited()));
                rResponse.AppendData(theBlock.getStationExitSide());
            }

            rResponse.AppendData(std::to_string(theBlock.getOccupiedBy()));

            //switch stuff
            if (theBlock.getSwitchList() == "")
            {
                rResponse.AppendData("-1 -1");
                rResponse.AppendData("-1");
            }
            else
            {
                rResponse.AppendData(theBlock.getSwitchList());
                rResponse.AppendData(std::to_string(theBlock.getCurrentSwitch()));
            }

            rResponse.AppendData(std::to_string(theTrack->getTrackHeater()));

            // Implement failure mode later
            rResponse.AppendData("None");

            // line name, block number, section, elevation, cumulative elevation
            // length, grade, speed limit, underground, stationName
            // ticketsSold, passengersBoarded, passengersExited, exit side, occupied by
            // switchList, currentSwitch, trackHeater, failure mode

            //Common::Request newRequest(Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN, theIntString);
            //TrackModel::serviceQueue.Push(newRequest);
			rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
			break;
		}
		case Common::RequestCode::TRACK_MODEL_GUI_SET_TRACK_HEATER:
        {
			std::string test = rRequest.GetData();
			int pos = test.find(" ");
			int trackId = std::stoi(test.substr(0, pos));

			printf("\ntest = %s\n", test.c_str());
			printf("\npos = %d\n", pos);
			printf("\ntrackId = %d\n", trackId);
			test.erase(0, pos + 1);

			int heaterInt = std::stoi(test);

			printf("\nheaterInt = %d\n", heaterInt);
            Track *theTrack = TrackInfo::GetInstance().getTrack(trackId);

			if (heaterInt == 0)
			{
				theTrack->setTrackHeater(false);
			}
			else
			{
				theTrack->setTrackHeater(true);
			}
			printf("test4");
			rResponse.AppendData(std::to_string(trackId));
            rResponse.AppendData(std::to_string(heaterInt));
			rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
			break;
        }
		case Common::RequestCode::TRACK_MODEL_GUI_TRACK_LAYOUT:
		{
			TrackModel::serviceQueue.Push(rRequest);
			rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
			break;
		}
        case Common::RequestCode::TRACK_MODEL_GUI_BLOCK:
		{
			TrackModel::serviceQueue.Push(rRequest);
			rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
			break;
		}
        default:
            std::cerr << "Invalid command " << static_cast<uint16_t>(rRequest.GetRequestCode())
                      << " received" << std::endl;
            rResponse.SetData("INVALID COMMAND");
            return;

    }
}
}
