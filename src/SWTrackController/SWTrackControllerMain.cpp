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

    	switch(req.GetRequestCode())
        {
            case Common::RequestCode::SWTRACK_DISPATCH_TRAIN:
            {


                std::string a =req.GetData().substr();

                reqSend.SetRequestCode(Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN);
                reqSend.SetData("");

                reqSend.AppendData(a);
                TrackModel::serviceQueue.Push(reqSend);


               // LOG_SW_TRACK_CONTROLLER("From ConnectionHandler.cpp (CTC_DISPATCH_TRAIN) : Sent Track C. Train %d to block %d",
			     //       pto_send->train_id, pto_send->destination_block);

                break;





            }




        }




    }
}

} // namespace SWTrackController
