/**
 * @file CTCTrainSystemUT.cpp
*/

// SYSTEM INCLUDES
#include "TrainSystem.hpp"

// C++ PROJECT INCLUDES
#include <catch2/catch.hpp>

/*
 * Test Singleton Constructor/Getter
 */
TEST_CASE( "Test TrainSystem Singleton Constructor", "[TrainSystem::GetInstance()]" )
{
	TrainSystem& pts = TrainSystem::GetInstance();  // Create instance
	REQUIRE(&TrainSystem::GetInstance() == &pts);
}