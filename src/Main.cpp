/**
 * @file Main.cpp
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cerr

// C++ PROJECT INCLUDES
#include "Server.hpp" // For Server
#include "../include/CTC/TrainSystem.h" // For CTC System
#include "CTC/TrainSystem.cpp"

int main()
{
    /* Module Specific Initializations */
    
    
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
