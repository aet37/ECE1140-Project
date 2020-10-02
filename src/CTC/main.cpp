#include "../../include/CTC/TrainSystem.h"
#include "TrainSystem.cpp"

int main()
{
	// Initialize system
	TrainSystem sys;

	// Create a train
	sys.printout();
	sys.create_new_train(LINE_BLUE);
	sys.printout();
}