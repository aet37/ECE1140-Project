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
		    	int ln = req.ParseData<int>(0);
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

			    // Set Suggested Speed and Authority
			    pto_send->command_speed = 55;
			    pto_send->authority = 3;
				pto_send->line_on = line_on;
			    // Set route
			    if(line_on == LINE_GREEN)
			    {
			    	pto_send->rout_switches = TrainSystem::GetInstance().green_route_switches;
			    	pto_send->route_blocks = TrainSystem::GetInstance().green_route_blocks;
			    }
			    else
			    {
				    pto_send->rout_switches = TrainSystem::GetInstance().red_route_switches;
				    pto_send->route_blocks = TrainSystem::GetInstance().red_route_blocks;
			    }

			    // Push Train Struct to Track controller queue
				reqSend.SetRequestCode(Common::RequestCode::SWTRACK_DISPATCH_TRAIN);  // Create request class to send
				reqSend.SetData("");    // Clear Previous Data

				// Add "train_di destination_block command_speed authority Line_on switch_arr" to send string
				reqSend.AppendData(std::to_string(pto_send->train_id));
				reqSend.AppendData(std::to_string(pto_send->destination_block));
			    reqSend.AppendData(std::to_string(pto_send->command_speed));
			    reqSend.AppendData(std::to_string(pto_send->authority));
			    if(pto_send->line_on == LINE_GREEN)
			    {
				    reqSend.AppendData("0");    // Send Line if Green
			    }
			    else
			    {
			    	reqSend.AppendData("1");    // Send Line if Red
			    }

			    if(pto_send->line_on == LINE_GREEN)
			    {
				    reqSend.AppendData("0001110100");
			    }
			    else
			    {
				    reqSend.AppendData("01111101000001");
			    }

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
				LOG_CTC("CTC received this: %s", req.GetData().c_str());
			    std::string green_occupancies = req.ParseData<std::string>(0);  // get green block occupancies
			    std::string red_occupancies = req.ParseData<std::string>(1);    // get red block occupancies
				green_occupancies.push_back('0');

			    for(int i = 0; i < TrainSystem::GetInstance().GetTrackArr(LINE_GREEN).size(); i++)
			    {
			    	if(green_occupancies.at(i) == '1')
				    {
			    		TrainSystem::GetInstance().SetTrackOccupied(i + 1, LINE_GREEN);
				    }
			    	else if(green_occupancies.at(i) == '0')
				    {
					    TrainSystem::GetInstance().SetTrackNotOccupied(i + 1, LINE_GREEN);
				    }
			    	else
				    {
			    		std::cout << req.GetData() << std::endl;
			    		throw std::logic_error("CTC::CTCMain.cpp : Track Controller sent invalid Track Occupancy Array (Green)");
				    }
			    }

			    for(int i = 0; i < TrainSystem::GetInstance().GetTrackArr(LINE_RED).size(); i++)
			    {
				    if(red_occupancies.at(i) == '1')
				    {
					    TrainSystem::GetInstance().SetTrackOccupied(i + 1, LINE_RED);
				    }
				    else if(red_occupancies.at(i) == '0')
				    {
					    TrainSystem::GetInstance().SetTrackNotOccupied(i + 1, LINE_RED);
				    }
				    else
				    {
					    std::cout << req.GetData() << std::endl;
					    throw std::logic_error("CTC::CTCMain.cpp : Track Controller sent invalid Track Occupancy Array (Red)");
				    }
			    }

			    // Update Train Positions based on updated track occupancies
			    TrainSystem::GetInstance().UpdateTrainPosition();
			    break;
		    }
		    // Get Switches from Track Controller
		    case Common::RequestCode::CTC_GET_SWITCHES:
		    {
			    std::string green_switches = req.ParseData<std::string>(0);  // get green switches
			    std::string red_switches = req.ParseData<std::string>(1);    // get red switches

			    for(int i = 0; i < TrainSystem::GetInstance().GetSwitchesArr(LINE_GREEN).size(); i++)
			    {
				    if(green_switches.at(i) == '1')
				    {
					    TrainSystem::GetInstance().SetSwitch(i + 1, LINE_GREEN, 1);
				    }
				    else if(green_switches.at(i) == '0')
				    {
					    TrainSystem::GetInstance().SetSwitch(i + 1, LINE_GREEN, 0);
				    }
				    else
				    {
					    std::cout << req.GetData() << std::endl;
					    throw std::logic_error("CTC::CTCMain.cpp : Track Controller sent invalid Switch Array (Green)");
				    }
			    }

			    for(int i = 0; i < TrainSystem::GetInstance().GetSwitchesArr(LINE_RED).size(); i++)
			    {
				    if(red_switches.at(i) == '1')
				    {
					    TrainSystem::GetInstance().SetSwitch(i + 1, LINE_RED, 1);
				    }
				    else if(red_switches.at(i) == '0')
				    {
					    TrainSystem::GetInstance().SetSwitch(i + 1, LINE_RED, 0);
				    }
				    else
				    {
					    std::cout << req.GetData() << std::endl;
					    throw std::logic_error("CTC::CTCMain.cpp : Track Controller sent invalid Switch Array (Red)");
				    }
			    }
			    break;
		    }
		    default:
		    	break;
	    }
    }
}

} // namespace CTC
