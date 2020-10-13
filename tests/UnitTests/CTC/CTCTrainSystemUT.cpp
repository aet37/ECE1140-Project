/**
 * @file CTCTrainSystemUT.cpp
*/

// SYSTEM INCLUDES
#include "TrainSystem.hpp"

// C++ PROJECT INCLUDES
#include <catch2/catch.hpp>


/*
 * TEMPORARY TEST CASE
 */
TEST_CASE( "Test TrainSystem ImportTrack and Constructor", "[TrainSystem::ImportTrackLayout()]" )
{
	TrainSystem::GetInstance(); //Activate constructor
	REQUIRE(TrainSystem::GetInstance().GetTrackArr().size() == 15); // Check that the size is 15 blocks
}




/*
 * Test Singleton Constructor/Getter
 */
TEST_CASE( "Test TrainSystem Singleton Constructor", "[TrainSystem::GetInstance()]" )
{
	TrainSystem& pts = TrainSystem::GetInstance();  // Create instance
	REQUIRE(&TrainSystem::GetInstance() == &pts);
}

/*
 * Test creating new train
 */
TEST_CASE( "Test Create New Train", "[TrainSystem::CreateNewTrain()]" )
{
	TrainSystem::GetInstance().CreateNewTrain(10);

	REQUIRE(TrainSystem::GetInstance().GetTrainArr().size() == 1);  // Check that the size is 1
	REQUIRE(TrainSystem::GetInstance().GetTrainArr()[0]->destination_block == 10);  // Check that the destination block is 10

	TrainSystem::GetInstance().CreateNewTrain(15);
	REQUIRE(TrainSystem::GetInstance().GetTrainArr().size() == 2);  // Check that the size is 1
	REQUIRE(TrainSystem::GetInstance().GetTrainArr()[1]->destination_block == 15);  // Check that the destination block is 15
}

/*
 * Test setting block to occupied
 */
TEST_CASE( "Test Set Track Occupied", "[TrainSystem::SetTrackOccupied()]" )
{
	TrainSystem::GetInstance(); // Activate class through constructor

	bool caught_error = false;  // Initialize variable to catch error
	try
	{
		TrainSystem::GetInstance().SetTrackOccupied(-1);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(caught_error);
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackOccupied(0);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(caught_error);      // Make sure exception was thrown
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackOccupied(1);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(!caught_error);     // Make sure exception was not thrown
	REQUIRE(TrainSystem::GetInstance().GetTrackArr()[0]->occupied == true); // Make sure that track 1 was set as occupied
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackOccupied(TrainSystem::GetInstance().GetTrackArr().size());
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(!caught_error);     // Make sure exception was not thrown
	REQUIRE(TrainSystem::GetInstance().GetTrackArr()[TrainSystem::GetInstance().GetTrackArr().size() - 1]->occupied == true); // Make sure that the last track is occupied
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackOccupied(TrainSystem::GetInstance().GetTrackArr().size() + 1);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(caught_error);     // Make sure exception was thrown
}

/*
 * Test setting block to not
 */
TEST_CASE( "Test Set Track Not Occupied", "[TrainSystem::SetTrackNotOccupied()]" )
{
	TrainSystem::GetInstance(); // Activate class through constructor

	bool caught_error = false;  // Initialize variable to catch error
	try
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(-1);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(caught_error);
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(0);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(caught_error);      // Make sure exception was thrown
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(1);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(!caught_error);     // Make sure exception was not thrown
	REQUIRE(TrainSystem::GetInstance().GetTrackArr()[0]->occupied == false); // Make sure that track 1 was set as occupied
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(TrainSystem::GetInstance().GetTrackArr().size());
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(!caught_error);     // Make sure exception was not thrown
	REQUIRE(TrainSystem::GetInstance().GetTrackArr()[TrainSystem::GetInstance().GetTrackArr().size() - 1]->occupied == false); // Make sure that the last track is occupied
	caught_error = false;

	try
	{
		TrainSystem::GetInstance().SetTrackNotOccupied(TrainSystem::GetInstance().GetTrackArr().size() + 1);
	}
	catch(std::logic_error e)
	{
		caught_error = true;
	}
	REQUIRE(caught_error);     // Make sure exception was thrown
}