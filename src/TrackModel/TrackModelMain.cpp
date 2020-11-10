/**
 * @file TrackModelMain.cpp
*/

// SYSTEM INCLUDES
#include <map>
#include <vector>

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

   // std::map<std::string, std::vector<uint32_t>>* pGreenLinePaths = new std::map<std::string, std::vector<uint32_t>>();
   // std::map<std::string, std::vector<uint32_t>>* pRedLinePaths = new std::map<std::string, std::vector<uint32_t>>();

   // initializeRouteMaps(*pGreenLinePaths, *pRedLinePaths);

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

                uint32_t trainId = req.ParseData<uint32_t>(0);
                uint32_t destinationBlock = req.ParseData<uint32_t>(1);
                uint32_t commandSpeed = req.ParseData<uint32_t>(2);
                bool authority = req.ParseData<bool>(3);
                uint32_t lineNumber = req.ParseData<uint32_t>(4);
                std::string switchPositions = req.ParseData<std::string>(5);




                std::string theIntString = std::to_string(trainId);
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
                if (test.find("Station\": \"") != std::string::npos){
                    pos = test.find("Station\": \"");
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

/*void initializeRouteMaps(std::map<std::string, std::vector<uint32_t>>& rGreenLineRoutes, std::map<std::string, std::vector<uint32_t>>& rRedLineRoutes)
{
    // # All the track controllers and the blocks they control
    //     self.red_line_controllers = [
    //         [1, 2, 3, 4, 5, 6, 7, 8, 9], # Switch between C and D @ block 9
    //         [0, 9, 10, 11, 12, 13, 14, 15],
    //         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], # Switch between A, E, and F @ block 16
    //         [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
    //         [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], # Switch between H and T @ block 27
    //         [72, 73, 74, 75, 76, 27, 28, 29, 30, 31, 32],
    //         [72, 73, 74, 75, 76, 28, 29, 30, 31, 32, 33], # Switch between R and H @ block 33
    //         [33, 34, 35, 36, 37],
    //         [34, 35, 36, 37, 38], # Switch between H and Q @ block 38
    //         [38, 39, 40, 41, 42, 43, 71, 70, 69, 68, 67],
    //         [39, 40, 41, 42, 43, 44, 71, 70, 69, 68, 67], # Switch between O and H @ block 44
    //         [44, 45, 46, 47, 48, 49, 50, 51],
    //         [45, 46, 47, 48, 49, 50, 51, 52], # Switch between J and N @ block 52
    //         [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]
    //     ]

    //     self.green_line_controllers = [
    //         [0, 62, 61, 60, 59], # Switch between J, K, and Yard @ block 62
    //         [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76],
    //         [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 101] + list(range(102, 151)), # Switch between M, N, and R @ block 77
    //         [77, 78, 79, 80, 81, 82, 83, 84],
    //         [85, 78, 79, 80, 81, 82, 83, 84], # Switch between N, O, and Q @ block 85
    //         [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
    //         list(range(101, 151)) + list(range(29, 58)), # Switch between Z, F, and G @ block 29
    //         [29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14],
    //         [28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13], # Switch between D, A, and C @ block 13
    //         [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    //         list(range(30, 59)), # Switch between I, J and Yard @ block 58
    //         [58, 59, 60, 61]
    //     ]

    std::vector<uint32_t> blocks = {0,
                                    62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                                    77, 78, 79, 80, 81, 82, 83, 84, 85,
                                    86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                                    85, 84, 83, 82, 81, 80, 79, 78, 77,
                                    101,
                                    102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                                    113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
                                    124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134,
                                    135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150,
                                    28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,
                                    12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1,
                                    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                                    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                                    0
                                    };
    rGreenLineRoutes.insert(std::pair<std::string, std::vector<uint32_t>>("0001110100", blocks));

    std::vector<uint32_t> base = {9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27};
    std::vector<uint32_t> choice1 = {28, 29, 30, 31, 32};
    std::vector<uint32_t> choice2 = {76, 75, 74, 73, 72};
    std::vector<uint32_t> base1 = {33, 34, 35, 36, 37, 38};

    std::vector<uint32_t> choice3 = {39, 40, 41, 42, 43};
    std::vector<uint32_t> choice4 = {71, 70, 69, 68, 67};
    std::vector<uint32_t> base2 = {44, 45, 46, 47, 48, 49, 50, 51, 52};

    std::vector<uint32_t> choice5 = {53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66};
    std::vector<uint32_t> choice6 = {66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53};
    std::vector<uint32_t> base3 = {52, 51, 50, 49, 48, 47, 46, 45, 44};

    std::vector<uint32_t> choice7 = {43, 42, 41, 40, 39};
    std::vector<uint32_t> choice8 = {67, 68, 69, 70, 71};
    std::vector<uint32_t> base4 = {38, 37, 36, 35, 34, 33};

    std::vector<uint32_t> choice9 = {32, 31, 30, 29, 28};
    std::vector<uint32_t> choice10 = {72, 73, 74, 75, 76};
    std::vector<uint32_t> base5 = {27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16};

    std::vector<uint32_t> choice11 = {1, 2, 3, 4, 5, 6, 7, 8, 9};

    std::vector<uint32_t> choice12 = {0};
    ///TODO: choice13 is where the train comes A->B->C->D instead of the yard. We are not accounting for this currently
    ///TODO: for now we will say it always enters yard
    std::vector<uint32_t> choice13 = {0};


    std::vector<uint32_t> choice14 = {15, 14, 13, 12, 11, 10};


    for (int i = 0; i < 2; i++)
    {
        if (i == 0)
        {
            base.insert(base.end(), choice1.begin(), choice1.end());
        }
        else
        {
            base.insert(base.end(), choice2.begin(), choice2.end());
        }
            base.insert(base.end(), base1.begin(), base1.end());
        for (int j = 0; j < 2; j++)
        {
            if (j == 0)
            {
            base.insert(base.end(), choice3.begin(), choice3.end());
            }
            else
            {
            base.insert(base.end(), choice4.begin(), choice4.end());
            }
            base.insert(base.end(), base2.begin(), base2.end());

            for (int k = 0;  k < 2; k++)
            {
                if (k == 0)
                {
                base.insert(base.end(), choice5.begin(), choice5.end());
                }
                else
                {
                base.insert(base.end(), choice6.begin(), choice6.end());
                }
                base.insert(base.end(), base3.begin(), base3.end());
                
                for (int l = 0; l < 2; l++)
                {
                    if (l == 0)
                    {
                    base.insert(base.end(), choice7.begin(), choice7.end());
                    }
                    else
                    {
                    base.insert(base.end(), choice8.begin(), choice8.end());
                    }
                    base.insert(base.end(), base4.begin(), base4.end());

                    for (int m = 0; m < 2; m++)
                    {
                        if (m == 0)
                        {
                        base.insert(base.end(), choice9.begin(), choice9.end());
                        }
                        else
                        {
                        base.insert(base.end(), choice10.begin(), choice10.end());
                        }
                        base.insert(base.end(), base5.begin(), base5.end());

                        for (int n = 0; n < 2; n++)
                        {
                            int p = 0;
                            if (m == 0)
                            {
                                base.insert(base.end(), choice11.begin(), choice11.end());
                                for (int o = 0; o < 2; o++)
                                {
                                    
                                    if (o == 0)
                                    {
                                        p = 0;
                                        base.insert(base.end(), choice12.begin(), choice12.end());
                                    }
                                    else
                                    {
                                        p = 1;
                                        base.insert(base.end(), choice13.begin(), choice13.end());
                                    }
                                }
                            }
                            else
                            {
                                base.insert(base.end(), choice14.begin(), choice14.end());
                            }
                            std::string switchPositions = std::to_string(i) + std::to_string(j) + std::to_string(k) + std::to_string(l) + std::to_string(m) + std::to_string(n) + std::to_string(p);
                            rRedLineRoutes.insert(std::pair<std::string, std::vector<uint32_t>>(switchPositions, blocks));
                        }
                    }
                }
            }

        }
    }
/**


        {1, 2, 3, 4, 5, 6, 7, 8, 9}
            {0}
            or
            {10, 11, 12, 13, 14, 15, 16}
        or
        {15, 14, 13, 12, 11, 10}

                                std::string switchPositions =
                                rRedLineRoutes.insert(std::pair<std::string, std::vector<uint32_t>>("01111101000001", blocks));

    blocks = {};
    rRedLineRoutes.insert(std::pair<std::string, std::vector<uint32_t>>("01111101000001", blocks));
    
}
*/

} // namespace TrackModel
