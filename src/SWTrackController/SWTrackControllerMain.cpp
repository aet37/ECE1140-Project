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

                uint32_t theInt = req.ParseData<uint32_t>(0);
                std::string theIntString = std::to_string(theInt);
                Common::Request newRequest(Common::RequestCode::TRACK_MODEL_DISPATCH_TRAIN, theIntString);
                TrackModel::serviceQueue.Push(newRequest);
                LOG_SW_TRACK_CONTROLLER("Track model dispatch train %s", theIntString.c_str());
                break;
 

               // LOG_SW_TRACK_CONTROLLER("From ConnectionHandler.cpp (CTC_DISPATCH_TRAIN) : Sent Track C. Train %d to block %d",
			     //       pto_send->train_id, pto_send->destination_block);

                break;





            }




        }




    }
}

} // namespace SWTrackController
