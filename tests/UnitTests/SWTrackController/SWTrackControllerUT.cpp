/**
 * @file SWTrackControllerUT.cpp
*/


// SYSTEM INCLUDES
#include "TrackSystem.hpp"

// C++ PROJECT INCLUDES
#include <catch2/catch_all.hpp>


/*
 * PLC uploader
 */
TEST_CASE( "PLC upload", "[TrackSystem::ImportPLCFile()]" )
{
	TrackSystem::GetInstance(); //Activate constructor
	REQUIRE(TrackSystem::GetInstance().GetPLCexist()== false); // Check that the plc file does not exist

	//Compiler not created yet otherwise there would be tests for when it is uploaded
}




/*
 * Test Singleton Constructor/Getter
 */
TEST_CASE( "Test TrackSystem Singleton Constructor", "[TrackSystem::GetInstance()]" )
{
	TrackSystem& pts = TrackSystem::GetInstance();  // Create instance
	REQUIRE(&TrackSystem::GetInstance() == &pts);
}

/*
 * Test creating new switch
 */
TEST_CASE( "Test Create New Switch", "[TrackSystem::CreateNewSwitch()]" )
{
	TrackSystem::GetInstance().CreateNewSwitch(1,2,7);


	REQUIRE(TrackSystem::GetInstance().GetOut(1).size() == 2);  // Check that the switch is made with out set to 2 by default
	

	TrackSystem::GetInstance().ChangeSwitchOut(1);
	REQUIRE(TrackSystem::GetInstance().GetOut(1) == 7);  // Check that the out block was set to 7




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