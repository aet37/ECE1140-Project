/**
 * @file Main.cpp
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cerr
#include <thread> // For std::thread

// C++ PROJECT INCLUDES
#include "Server.hpp" // For Server
#include "Logger.hpp" // For LOG macros
#include "CTCMain.hpp" // For CTC::moduleMain
#include "HWTrackControllerMain.hpp" // For HWTrackController::moduleMain
#include "SWTrackControllerMain.hpp" // For SWTrackController::moduleMain
#include "TrackModelMain.hpp" // For HWTrackController::moduleMain
#include "TrainModelMain.hpp" // For HWTrackController::moduleMain
#include "HWTrainControllerMain.hpp" // For HWTrainController::moduleMain
#include "SWTrainControllerMain.hpp" // For SWTrainController::moduleMain
#include "Timekeeper.hpp" // For Common::Timekeeper

int main()
{
    // Spawn threads
    std::thread ctcThread(CTC::moduleMain);
    std::thread hwTrackControllerThread(HWTrackController::moduleMain);
    std::thread swTrackControllerThread(SWTrackController::moduleMain);
    std::thread trackModelThread(TrackModel::moduleMain);
    std::thread trainModelThread(TrainModel::moduleMain);
    std::thread hwTrainControllerThread(HWTrainController::moduleMain);
    std::thread swTrainControllerThread(SWTrainController::moduleMain);
    std::thread timeKeeperThread([]() { Common::Timekeeper::GetInstance().KeepTime(); });

    LOG_SERVER("Server Starting...");
    try
    {
        boost::asio::io_service io_service;
        Server server(io_service);
        io_service.run();
    }
    catch (std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    return 0;
}
