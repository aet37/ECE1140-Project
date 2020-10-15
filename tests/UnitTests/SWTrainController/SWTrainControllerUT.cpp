/**
 * @file SWTrackControllerUT.cpp
*/

// SYSTEM INCLUDES
#include "ControlSystem.h"

// C++ PROJECT INCLUDES
#include <catch2/catch_all.hpp>

/*
 * Test creation of new singleton controller
 */
TEST_CASE( "Test ControlSystem createNewController", "[ControlSystem::createNewController(int, int, int, int)]" )
{
	Controller* p_testPtr = ControlSystem::createNewController(3,4,5,6);
	
	// Use getControllerInstance method to test creation
	REQUIRE(p_testPtr == ControlSystem::getControllerInstance(0));
}
