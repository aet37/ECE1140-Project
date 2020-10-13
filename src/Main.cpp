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

int main()
{
    // Spawn threads
    std::thread ctcThread(CTC::moduleMain);
    std::thread hwTrackControllerThread(HWTrackController::moduleMain);

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
