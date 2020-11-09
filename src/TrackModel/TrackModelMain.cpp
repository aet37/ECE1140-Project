/**
 * @file TrackModelMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "TrackModelMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"
#include "SWTrackControllerMain.hpp"
#include "TrainModelMain.hpp"
#include "TrackInfo.hpp"

namespace TrackModel
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_TRACK_MODEL("Thread starting...");

    while (true)
    {
        Common::Request req = serviceQueue.Pop();

        switch(req.GetRequestCode())
        {
           /* case Common::RequestCode::GET_POSITION_FROM_TRAINM: 
            {
                uint32_t position = std::stoi(req.GetData());

                std::string occupancy_send = std::to_string(position);
                
                Common::Request newRequest(Common::RequestCode::SWTRACK_GET_OCCUPANCY, occupancy_send);
                SWTrackController::serviceQueue.Push(newRequest);
                // Recieve position in ??? units from Train Model
                // Hardcoding to 75 units for now
                //req.SetData("75");
                break;
            }*/
            //case Common::RequestCode::SEND_TRACK_OCCUPANCY_TO_SW_TRACK_C:
            //{
                
            //    break;

            //}
            case Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN:
            {
                // train id
                // destination block
                // command speed
                // authority
                // line 0 for green, 1 for red
                // switch positions
                uint32_t theInt = req.ParseData<uint32_t>(0);
                std::string theIntString = std::to_string(theInt);
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_DISPATCH_TRAIN, theIntString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_TRACK_MODEL("Track model dispatch train %s", theIntString.c_str());
                break;
            }
            case Common::RequestCode::TRACK_MODEL_GUI_TRACK_LAYOUT:
            {
                // get line name from string
                std::string test = req.GetData();
                std::string gettingLineName = test.erase(0, 11);
                int pos =  test.find('\"');
                std::string lineName = test.substr(0, pos); 
                test.erase(0, pos + 14);

                // get track number from string
                pos = test.find(',');
                std::string trackNumberString = test.substr(0, pos);
                int trackNumber = stoi(trackNumberString);
                test.erase(0, pos + 18); // 76} 

                // get total blocks from string
                pos = test.find('}');
                std::string totalBlockString = test.substr(0, pos);
                int totalBlocks = stoi(totalBlockString);

                // add track to TrackInfo
                TrackInfo::GetInstance().AddTrackLayout(lineName, trackNumber, totalBlocks);

                break;
            }
            case Common::RequestCode::TRACK_MODEL_GUI_BLOCK:
            {
                std::string test = req.GetData();
                // get the track number so we can get the track
                test.erase(0, 10);
                int pos = test.find(',');
                std::string gettingTrackNumber = test.substr(0, pos);
                int trackNumberInt = stoi(gettingTrackNumber);

                // grab track using track number
                Track *theTrack = TrackInfo::GetInstance().getTrack(trackNumberInt);

                // get number of block, convert to int
                test.erase(0, pos + 2);
                pos = test.find(',');
                std::string blockNumberString = test.substr(0, pos);
                int blockNumber = stoi(blockNumberString);
                test.erase(0, pos + 12);

                // get length of block, convert to double
                pos = test.find(',');
                std::string blockLengthString = test.substr(0, pos);
                double blockLength = stod(blockLengthString);
                test.erase(0, pos + 11);

                // get grade, convert to double
                pos = test.find(',');
                std:: string blockGradeString = test.substr(0, pos);
                double blockGrade = stod(blockGradeString);
                test.erase(0, pos + 17);

                // get get speed limit, convert to int
                pos = test.find(',');
                std::string blockSpeedLimitString = test.substr(0, pos);
                int blockSpeedLimit = stoi(blockSpeedLimitString);
                test.erase(0, pos + 15);

                // get elevation, convert to double
                pos = test.find(',');
                std::string blockElevationString = test.substr(0, pos);
                double blockElevation = stod(blockElevationString);
                test.erase(0, pos + 26);

                // get cumulative elevation, convert to double
                pos = test.find(',');
                std::string blockCumulativeElevationString = test.substr(0, pos);
                double blockCumulativeElevation = stod(blockCumulativeElevationString);

                // get StationInfo
                if (test.find('Station\": \"') != std::string::npos){
                    pos = test.find('Station\": \"');
                    test.erase(0, pos + 11);
                    //std::string stationInfo
                }



                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }


    }



}

} // namespace TrackModel
