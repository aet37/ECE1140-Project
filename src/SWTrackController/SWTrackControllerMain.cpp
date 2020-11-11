/**
 * @file SWTrackControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrackControllerMain.hpp" // Header for functions
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

    Common::Request reqSend;

    while(true)
    {
        Common::Request req = serviceQueue.Pop();

	    // Clear Request code object if used
	    reqSend.SetRequestCode(Common::RequestCode::ERROR); // Clear request code object
	    reqSend.SetData("");    // Clear Previous Data
        TrackSystem main;

    	switch(req.GetRequestCode())
        {
            case Common::RequestCode::SWTRACK_DISPATCH_TRAIN:
            {
                std::string indata = req.GetData();
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
                bool line = req.GetData().at(0);
                std::string block = req.GetData().substr(2,2);
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




        }

        

        






    }

}

} // namespace SWTrackController
