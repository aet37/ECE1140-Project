#include "TrainSystem.hpp"
#include "BufferFunctions.hpp"
#include <chrono>
#include <thread>

int main()
{
	int loc = 1;
	while(1)
	{
		std::chrono::seconds dura(5);
		std::this_thread::sleep_for(dura);

		TrainLocationBuffer_CTC(loc);
		if(loc == 10)
		{
			loc = 1;
		}
		else
		{
			loc++;
		}
	}
}