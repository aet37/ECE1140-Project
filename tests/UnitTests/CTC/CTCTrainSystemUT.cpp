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