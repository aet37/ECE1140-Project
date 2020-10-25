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
TEST_CASE( "Test ControlSystem createNewController", "[ControlSystem::createNewController(int, int, int)]" )
{
    ControlSystem testSystem(1,2,4);
	Controller* p_testPtr = testSystem.createNewController(3,4,6);
	
	// Use getControllerInstance method to test creation
	REQUIRE(p_testPtr == testSystem.getControllerInstance(1));
}

/*
 * Test getControllerInstance by creating multiple controllers
 */
TEST_CASE( "Test ControlSystem getControllerInstance", "[ControlSystem::getControllerInstance(int)]")
{
    // Create two controllers
    ControlSystem testSystem(3,4,6);
    testSystem.createNewController(1,2,8);
    Controller* p_testPtr = testSystem.getControllerInstance(0);
    Controller* p_testPtr2 = testSystem.getControllerInstance(1);

    // Test getControllerInstance using created pointers
    REQUIRE(p_testPtr != testSystem.getControllerInstance(1));
    REQUIRE(p_testPtr2 != testSystem.getControllerInstance(0));
}