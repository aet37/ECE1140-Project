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

                std::string indata = receivedReq.GetData();
                bool line;
                std::vector<bool> switchpos;

                for(int i=0;i<indata.length()-1;i++)
                {
                    int count=0;
                    if(indata[i]==' ')
                    {
                        count++;

                        if(count==4)
                        {
                            line=indata[i+1];
                        }
                        if(count==5)
                        {
    
                            for(int j=i+1;i<indata.length()-1;i++)
                            {
                            switchpos[j]=indata[j];
                            }
                        }
                    }
                }
                main.inputPositions(switchpos,line);
                if(line==0)
                {
                    Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "switch " + switchpos[0]);
                    HWTrackController::HWTrackControllerRequestManager reqManager;
                    Common::Response a;
                    reqManager.HandleRequest(newReq, a);
                }


                
                Common::Request newRequest(Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN );
                newRequest.SetData(indata);
                TrackModel::serviceQueue.Push(newRequest);
                //LOG_SW_TRACK_CONTROLLER("SWTrackController dispatch train %s", theIntString.c_str());
                break;

                
 

               // LOG_SW_TRACK_CONTROLLER("From ConnectionHandler.cpp (CTC_DISPATCH_TRAIN) : Sent Track C. Train %d to block %d",
			     //       pto_send->train_id, pto_send->destination_block);

                break;
            }


            case Common::RequestCode::SWTRACK_SET_TRACK_OCCUPANCY:
            {
                bool line = receivedReq.GetData().at(0);
                std::string block = receivedReq.GetData().substr(2,2);
                int blockNum = stoi(block);

                if(line ==0)
                {
                    if(blockNum==62)
                    {
                        Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block62Occupancy " + 1);
                        HWTrackController::HWTrackControllerRequestManager reqManager;
                        Common::Response a;
                        reqManager.HandleRequest(newReq, a);
                    }

                    else if(blockNum==61)
                    {
                        Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block61Occupancy " + 1);
                        HWTrackController::HWTrackControllerRequestManager reqManager;
                        Common::Response a;
                        reqManager.HandleRequest(newReq, a);
                    }

                    else if(blockNum==60)
                    {
                        Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block60Occupancy " + 1);
                        HWTrackController::HWTrackControllerRequestManager reqManager;
                        Common::Response a;
                        reqManager.HandleRequest(newReq, a);
                    }

                    else if(blockNum==59)
                    {
                        Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block59Occupancy " + 1);
                        HWTrackController::HWTrackControllerRequestManager reqManager;
                        Common::Response a;
                        reqManager.HandleRequest(newReq, a);
                    }

                     else if (blockNum==0)
                    {
                        Common::Request newReq(Common::RequestCode::HWTRACK_SET_TAG_VALUE, "block0Occupancy " + 1);
                        HWTrackController::HWTrackControllerRequestManager reqManager;
                         Common::Response a;
                        reqManager.HandleRequest(newReq, a);
                    }
                }
                else
                {
                    main.updateOccupied(line, blockNum);
                }

                Common::Request OccUpdate(Common::RequestCode::CTC_GET_OCCUPANCIES);
                OccUpdate.SetData(main.makeOccupancies());
                CTC::serviceQueue.Push(OccUpdate);

                Common::Request SwitchUpdate(Common::RequestCode::CTC_GET_SWITCHES);
                SwitchUpdate.SetData(main.makePositions());
                CTC::serviceQueue.Push(SwitchUpdate);

                int switchMaybeChanged= main.didSwitchMove();
                bool singleSwitchPosition;
                bool thing;

                if(switchMaybeChanged<14)
                {
                    singleSwitchPosition= main.getSinglePosition(switchMaybeChanged);
                    Common::Request SwitchUpdateTM(Common::RequestCode::TRACK_MODEL_UPDATE_SWITCH_POSITIONS);
                    std::string out; 
                    if (switchMaybeChanged<7)
                    {
                        thing = 0;
                    }
                    else
                    {
                        thing = 1;
                    }
                    
                    out+= thing + ' ' + switchMaybeChanged + ' ' + singleSwitchPosition;
                    SwitchUpdateTM.SetData(out);

                    TrackModel::serviceQueue.Push(SwitchUpdateTM);
                }

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
            default:
                ASSERT(false, "Unhandled request code %d", static_cast<uint16_t>(receivedReq.GetRequestCode()));
                break;
        }

    }

}

} // namespace SWTrackController
