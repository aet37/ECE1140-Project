/**
 * @file Main.cpp
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cerr

// C++ PROJECT INCLUDES
#include "Server.hpp" // For Server

int main()
{
    // Module Specific Initializations
    
    
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
