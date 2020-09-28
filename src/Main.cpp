/**
 * @file Main.cpp
*/

// SYSTEM INCLUDES

// C++ PROJECT INCLUDES
#include "Server.hpp"


int main()
{
	try
    {
		boost::asio::io_service io_service;
		Server server(io_service);
		io_service.run();
    }
    catch (std::exception& e)
    {
		std::cerr << e.what() << endl;
    }
}
