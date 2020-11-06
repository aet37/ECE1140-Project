/**
 * @file CTCMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "CTCMain.hpp" // Header for functions
#include "SWTrackControllerMain.hpp"    // For sending information to the Train Controller
#include "Logger.hpp" // For LOG macros

namespace CTC
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_CTC("Thread starting...");

    // Create request object to be able to push on other queues
	Common::Request reqSend;

    while(true)
    {
    	Common::Request req = serviceQueue.Pop();

	    // Clear Request code object if used
	    reqSend.SetRequestCode(Common::RequestCode::ERROR); // Clear request code object
	    reqSend.SetData("");    // Clear Previous Data

    	switch(req.GetRequestCode())
	    {
    		// Dispatch Train from GUI
		    case Common::RequestCode::CTC_GUI_DISPATCH_TRAIN:
		    {
		    	// Get Line train is on
		    	int ln = std::stoi(req.GetData().substr(0, 1));
		    	Line line_on;
		    	if(ln == 0)
			    {
		    		line_on = LINE_GREEN;
			    }
		    	else
			    {
		    		line_on = LINE_RED;
			    }

			    // Get block train was dispatched to
			    std::string str_block = req.GetData().substr(10, req.GetData().size() - 10);
			    // Convert block to integer
			    int block_to = std::stoi(str_block);

			    // Call TrainSystem singleton instance to create a new train
			    Train *pto_send;
			    pto_send = TrainSystem::GetInstance().CreateNewTrain(block_to,line_on);

			    // Push Train Struct to Track controller queue
				reqSend.SetRequestCode(Common::RequestCode::SWTRACK_DISPATCH_TRAIN);  // Create request class to send
				reqSend.SetData("");    // Clear Previous Data

				// Add "train_di destination_block command_speed authority" to send string
				reqSend.AppendData(std::to_string(pto_send->train_id));
				reqSend.AppendData(std::to_string(pto_send->destination_block));
			    reqSend.AppendData(std::to_string(pto_send->command_speed));
			    reqSend.AppendData(std::to_string(pto_send->authority));

			    SWTrackController::serviceQueue.Push(reqSend);  // Push request to SW Track Controller Queue

			    // Log action
			    LOG_CTC("From ConnectionHandler.cpp (CTC_DISPATCH_TRAIN) : Sent Track C. Train %d to block %d",
			            pto_send->train_id, pto_send->destination_block);

			    pto_send = nullptr;           // Make pointer null
			    break;
		    }
			// Get Occupancies from Track Controller
	    	case Common::RequestCode::CTC_GET_OCCUPANCIES:
		    {
			    int block_location = std::stoi(req.GetData());  // get block location as integer
				/*
			    // set the block passed in as occupied
			    TrainSystem::GetInstance().SetTrackOccupied(block_location);

			    // set previous blocks as not occupied
			    if(block_location == 1)
			    {
				    return;
			    }
			    else if(block_location == 11)
			    {
				    TrainSystem::GetInstance().SetTrackNotOccupied(5);

				    // Log what was done
				    LOG_CTC("From TrainLocationBuffer_CTC() : Block %d set occupied, Block 5 set not occupied", block_location);
			    }
			    else
			    {
				    TrainSystem::GetInstance().SetTrackNotOccupied(block_location - 1);

				    // Log what was done
				    LOG_CTC("From TrainLocationBuffer_CTC() : Block %d set occupied, Block %d set not occupied", block_location, block_location - 1);

			    }
			    */
			    break;
		    }
		    default:
		    	break;
	    }
    }
}

} // namespace CTC
