/**
 * @file ControllerUT.cpp
*/

// SYSTEM INCLUDES
#include "Controller.h"

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

/*
 * Test getControllerInstance by creating multiple controllers
 */
TEST_CASE( "Test ControlSystem getControllerInstance", "[ControlSystem::getControllerInstance(int)]")
{
    // Create two controllers
    Controller* p_testPtr = ControlSystem::createNewController(3,4,5,6);
    Controller* p_testPtr2 = ControlSystem::createNewController(1,2,7,8);

    // Test getControllerInstance using created pointers
    REQUIRE(p_testPtr = ControlSystem::getControllerInstance(0));
    REQUIRE(p_testPtr2 = ControlSystem::getControllerInstance(1));
}