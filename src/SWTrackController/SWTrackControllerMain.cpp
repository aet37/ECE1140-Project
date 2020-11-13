/**
 * @file SWTrackControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrackControllerMain.hpp" // Header for functions
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // For LOG macros
#include "TrackModelMain.hpp"
#include "CTCMain.hpp"
#include <ctype.h>
#include <TrackSystem.hpp>
#include <HWTrackControllerRequestManager.hpp>
#include <Response.hpp>




namespace SWTrackController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_SW_TRACK_CONTROLLER("Thread starting...");

    while(true)
    {
        Common::Request reqSend;
	    // Clear Request code object if used
	    reqSend.SetRequestCode(Common::RequestCode::ERROR); // Clear request code object
	    reqSend.SetData("");    // Clear Previous Data
        TrackSystem main;

        Common::Request receivedReq = serviceQueue.Pop();

    	switch(receivedReq.GetRequestCode())
        {
            case Common::RequestCode::SWTRACK_DISPATCH_TRAIN:
            {
                LOG_SW_TRACK_CONTROLLER("SWTrackController received: %s", receivedReq.GetData().c_str());
                // Parse stuff from the CTC
                uint32_t trainId = receivedReq.ParseData<uint32_t>(0);
                uint32_t destinationBlock = receivedReq.ParseData<uint32_t>(1);
                uint32_t suggestedSpeed = receivedReq.ParseData<uint32_t>(2);
                uint32_t authority = receivedReq.ParseData<uint32_t>(3);
                uint32_t line = receivedReq.ParseData<uint32_t>(4);
                std::string switchPositionsString = receivedReq.ParseData<std::string>(5);

                std::vector<bool> switchPositions;

                for (int i = 0; i < switchPositionsString.size(); i++)
                {
                    switchPositions.push_back(switchPositionsString[i]);
                }

                main.inputPositions(switchPositions, line);

                if (line == 0)
                {
                    //LOG_SW_TRACK_CONTROLLER("SWTrackController sending HWTrack: %s", switchPositionsString[0].c_str());
                    Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "switch " + switchPositionsString[0]);
                    HWTrackController::HWTrackControllerRequestManager reqManager;
                    Common::Response a;
                    reqManager.HandleRequest(newReq, a);
                }

                LOG_SW_TRACK_CONTROLLER("SWTrackController sent: %s", receivedReq.GetData().c_str());
                Common::Request newRequest(Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN );
                newRequest.SetData(receivedReq.GetData());
                TrackModel::serviceQueue.Push(newRequest);
                break;
            }
            case Common::RequestCode::SWTRACK_SET_TRACK_OCCUPANCY:
            {
                
                /**
                 * Receiving this information:
                 * uint32_t lineId
                 * uint32_t blockId
                 * bool occupancy (0 - unoccupied, 1 - occupied)
                */
                LOG_SW_TRACK_CONTROLLER("SWTRACK_SET_TRACK_OCCUPANCY Received: %s", receivedReq.GetData().c_str());
                uint32_t line = receivedReq.ParseData<uint32_t>(0);
                uint32_t blockNum = receivedReq.ParseData<uint32_t>(1);
                bool occupancy = receivedReq.ParseData<bool>(2);
                // main.updateOccupied(line, blockNum);

                static std::string redLineOccupancies = "0000000000000000000000000000000000000000000000000000000000000000000000000000";
                static std::string greenLineOccupancies = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000";

                if (blockNum == 62)
                {
                    Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "b62O 1");
                    HWTrackController::HWTrackControllerRequestManager reqManager;
                    Common::Response a;
                    reqManager.HandleRequest(newReq, a);
                }

                if (line == 0)
                {
                    if (occupancy)
                    {
                        greenLineOccupancies[blockNum - 1] = '1';
                    }
                    else
                    {
                        greenLineOccupancies[blockNum - 1] = '0';
                    }
                }
                else
                {
                    if (occupancy)
                    {
                        redLineOccupancies[blockNum - 1] = '1';
                    }
                    else
                    {
                        redLineOccupancies[blockNum - 1] = '0';
                    }
                }

                LOG_SW_TRACK_CONTROLLER("SWTrackController green occupancies = %s", greenLineOccupancies.c_str());
                LOG_SW_TRACK_CONTROLLER("SWTrackController red occupancies = %s", redLineOccupancies.c_str());

                Common::Request OccUpdate(Common::RequestCode::CTC_GET_OCCUPANCIES);
                OccUpdate.AppendData(greenLineOccupancies);
                OccUpdate.AppendData(redLineOccupancies);
                // OccUpdate.AppendData(main.makeOccupancies());
                // OccUpdate.AppendData("0000000000000000000000000000000000000000000000000000000000000000000000");
                CTC::serviceQueue.Push(OccUpdate);
                LOG_SW_TRACK_CONTROLLER("Done sending occupancies");

                // LOG_SW_TRACK_CONTROLLER("SWTrackController sent CTC Block Occupancies: %s", main.makePositions().c_str());

                // Common::Request SwitchUpdate(Common::RequestCode::CTC_GET_SWITCHES);
                // SwitchUpdate.SetData(main.makePositions());
                // CTC::serviceQueue.Push(SwitchUpdate);


                // if(line == 0)
                // {
                //     LOG_SW_TRACK_CONTROLLER("");
                //     // if(blockNum==62)
                //     // {
                //     //     Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block62Occupancy " + 1);
                //     //     HWTrackController::HWTrackControllerRequestManager reqManager;
                //     //     Common::Response a;
                //     //     reqManager.HandleRequest(newReq, a);
                //     // }

                //     // else if(blockNum==61)
                //     // {
                //     //     Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block61Occupancy " + 1);
                //     //     HWTrackController::HWTrackControllerRequestManager reqManager;
                //     //     Common::Response a;
                //     //     reqManager.HandleRequest(newReq, a);
                //     // }

                //     // else if(blockNum==60)
                //     // {
                //     //     Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block60Occupancy " + 1);
                //     //     HWTrackController::HWTrackControllerRequestManager reqManager;
                //     //     Common::Response a;
                //     //     reqManager.HandleRequest(newReq, a);
                //     // }

                //     // else if(blockNum==59)
                //     // {
                //     //     Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block59Occupancy " + 1);
                //     //     HWTrackController::HWTrackControllerRequestManager reqManager;
                //     //     Common::Response a;
                //     //     reqManager.HandleRequest(newReq, a);
                //     // }

                //     //  else if (blockNum==0)
                //     // {
                //     //     Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block0Occupancy " + 1);
                //     //     HWTrackController::HWTrackControllerRequestManager reqManager;
                //     //      Common::Response a;
                //     //     reqManager.HandleRequest(newReq, a);
                //     // }
                // }
                // else
                // {
                //     main.updateOccupied(line, blockNum);
                // }

                // LOG_SW_TRACK_CONTROLLER("SWTrackController sent CTC Block Occupancies: %s", main.makeOccupancies().c_str());

                // Common::Request OccUpdate(Common::RequestCode::CTC_GET_OCCUPANCIES);
                // OccUpdate.SetData(main.makeOccupancies());
                // CTC::serviceQueue.Push(OccUpdate);

                // LOG_SW_TRACK_CONTROLLER("SWTrackController sent CTC Block Occupancies: %s", main.makePositions().c_str());

                // Common::Request SwitchUpdate(Common::RequestCode::CTC_GET_SWITCHES);
                // SwitchUpdate.SetData(main.makePositions());
                // CTC::serviceQueue.Push(SwitchUpdate);

                // int switchMaybeChanged= main.didSwitchMove();
                // bool singleSwitchPosition;
                // bool thing;

                // if(switchMaybeChanged<14)
                // {
                //     singleSwitchPosition= main.getSinglePosition(switchMaybeChanged);
                //     Common::Request SwitchUpdateTM(Common::RequestCode::TRACK_MODEL_UPDATE_SWITCH_POSITIONS);
                //     std::string out; 
                //     if (switchMaybeChanged<7)
                //     {
                //         thing = 0;
                //     }
                //     else
                //     {
                //         thing = 1;
                //     }
                    
                //     out+= thing + ' ' + switchMaybeChanged + ' ' + singleSwitchPosition;
                //     SwitchUpdateTM.SetData(out);

                //     TrackModel::serviceQueue.Push(SwitchUpdateTM);
                // }

                
                break;
            }
            case Common::RequestCode::SWTRACK_UPDATE_AUTHORITY:
            case Common::RequestCode::SWTRACK_SET_TRACK_SIGNAL:
            case Common::RequestCode::SWTRACK_UPDATE_COMMAND_SPEED:
            case Common::RequestCode::SWTRACK_SET_TRACK_STATUS:
            case Common::RequestCode::SWTRACK_SET_SWITCH_POSITION:
            case Common::RequestCode::SWTRACK_SET_TRACK_FAILURE:
            case Common::RequestCode::SWTRACK_SET_CROSSING:
            case Common::RequestCode::SWTRACK_SET_TRACK_HEATER:


            
            case Common::RequestCode::START_DOWNLOAD:
            case Common::RequestCode::END_DOWNLOAD:
            case Common::RequestCode::CREATE_TAG:
            case Common::RequestCode::CREATE_TASK:
            case Common::RequestCode::CREATE_ROUTINE:
            case Common::RequestCode::CREATE_RUNG:
            case Common::RequestCode::CREATE_INSTRUCTION:
            case Common::RequestCode::SET_TAG_VALUE:
            case Common::RequestCode::GET_TAG_VALUE:
            	break;
            default:
                ASSERT(false, "Unhandled request code %d", static_cast<uint16_t>(receivedReq.GetRequestCode()));
                break;
        }

    }

}

} // namespace SWTrackController
