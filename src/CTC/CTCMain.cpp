/**
 * @file CTCMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "CTCMain.hpp" // Header for functions
#include "SWTrainControllerMain.hpp"    // For sending information to the Train Controller
#include "Logger.hpp" // For LOG macros

namespace CTC
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_CTC("Thread starting...");

    while(true)
    {
    	Common::Request req = serviceQueue.Pop();

    	switch(req.GetRequestCode())
	    {
		    case Common::RequestCode::CTC_DISPATCH_TRAIN: {
			    // Get block train was dispatched to
			    std::string str_block = req.GetData().substr(0, 2);

			    // Convert block to integer
			    int block_to = std::stoi(str_block);

			    // Call TrainSystem singleton instance to create a new train
			    Train *pto_send;
			    pto_send = TrainSystem::GetInstance().CreateNewTrain(block_to);

			    // Push Train Struct to Track controller queue

			    // Log action
			    LOG_CTC("From ConnectionHandler.cpp (CTC_DISPATCH_TRAIN) : Sent Track C. Train %d to block %d",
			            pto_send->train_id, pto_send->destination_block);

			    // Make pointer null
			    pto_send = nullptr;
			    break;
		    }

	    	case Common::RequestCode::CTC_SEND_OCCUPANCIES:
	    	{
			    break;
		    }
		    default:
		    	break;
	    }
    }
}

} // namespace CTC
