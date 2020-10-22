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
TEST_CASE( "Test Controller default constructor", "[Controller::Controller()]" )
{
	Controller testObj;
	
	// Use getPowerCommand method to test creation of default object
	REQUIRE(testObj.getPowerCommand() == 0);
}

/*
 * Test initialized constructor and set Kp
 */
TEST_CASE( "Test Initialized constructor", "[Controller::Controller(int, int, int, int)]")
{
    // Create new controller with initialized command speed, current speed, speed limit, and authority
    Controller testObj(3,4,5,6);
    // Set Kp and calculate power
    testObj.setKp(3);
    testObj.calculatePower();

    // Test initialized controller by checking calculated power value
    REQUIRE(testObj.getPowerCommand() == (3*3));
}

/*
 * Test setKi and calculatePower
 */
TEST_CASE( "Test setKi and calculatePower", "[Controller::setKi(int), Controller::calculatePower()]")
{
    // Create new controller
    Controller testObj(3,4,5,6);

    // Set Kp and Ki
    testObj.setKp(3);
    testObj.setKi(2);

    // Calculate power
    testObj.calculatePower();
    REQUIRE(testObj.getPowerCommand() == 15);

    // Input a new command speed and recalculate power;
    testObj.setCommandSpeed(9);
    REQUIRE(testObj.getPowerCommand() == 15);
    testObj.calculatePower();
    REQUIRE(testObj.getPowerCommand() == 45);
}

/*
 * Test setCommandSpeed and getCommandSpeed
 */
TEST_CASE( "Test setCommandSpeed(int) and getCommandSpeed()", "[Controller::setCommandSpeed(int), Controller::getCommandSpeed()]")
{
    // Create new Controller
    Controller testObj;
    
    // Test default value of command speed
    REQUIRE(testObj.getCommandSpeed() == 0);

    // Set new value for command speed
    testObj.setCommandSpeed(5);

    // Test new value of command speed
    REQUIRE(testObj.getCommandSpeed() == 5);

    // Test with double value
    testObj.setCommandSpeed(3.1);
    REQUIRE(testObj.getCommandSpeed() == 3);
}

/*
 * Test setCurrentSpeed and getCurrentSpeed
 */
TEST_CASE( "Test setCurrentSpeed(int) and getCurrentSpeed()", "[Controller::setCurrentSpeed(int), Controller::getCurrentSpeed()]")
{
    // Create new Controller
    Controller testObj;
    
    // Test default value of current speed
    REQUIRE(testObj.getCurrentSpeed() == 0);

    // Set new value for current speed
    testObj.setCurrentSpeed(5);

    // Test new value of current speed
    REQUIRE(testObj.getCurrentSpeed() == 5);

    // Test with double value
    testObj.setCurrentSpeed(3.3);
    REQUIRE(testObj.getCurrentSpeed() == 3);
}

/*
 * Test setSpeedLimit and getSpeedLimit
 */
TEST_CASE( "Test setSpeedLimit(int) and getSpeedLimit()", "[Controller::setSpeedLimit(int), Controller::getSpeedLimit()]")
{
    // Create new Controller
    Controller testObj;
    
    // Test default value of speed limit
    REQUIRE(testObj.getSpeedLimit() == 0);

    // Set new value for speed limit
    testObj.setSpeedLimit(5);

    // Test new value of speed limit
    REQUIRE(testObj.getSpeedLimit() == 5);

    // Test with double value
    testObj.setSpeedLimit(3.6);
    REQUIRE(testObj.getSpeedLimit() == 3);
}

/*
 * Test setAuthority and getAuthority
 */
TEST_CASE( "Test setAuthority(int) and getAuthority()", "[Controller::setAuthority(int), Controller::getAuthority()]")
{
    // Create new Controller
    Controller testObj;
    
    // Test default value of authority
    REQUIRE(testObj.getAuthority() == 0);

    // Set new value for authority
    testObj.setAuthority(5);

    // Test new value of authority
    REQUIRE(testObj.getAuthority() == 5);

    // Test with double value
    testObj.setAuthority(3.8);
    REQUIRE(testObj.getAuthority() == 3);
}

/*
 * Test door toggle
 */
TEST_CASE( "Test toggleDoors", "[Controller::toggleDoors()]")
{
    // Create new controller
    Controller testObj;
    // Open doors
    REQUIRE(testObj.toggleDoors() == 1);
    // Close doors
    REQUIRE(testObj.toggleDoors() == 0);
    // Open doors one more time
    REQUIRE(testObj.toggleDoors() == 1);
}

/*
 * Test light toggle
 */
TEST_CASE( "Test toggleLights", "[Controller::toggleLights()]")
{
    // Create new controller
    Controller testObj;
    // Turn lights on
    REQUIRE(testObj.toggleLights() == 1);
    // Turn lights off
    REQUIRE(testObj.toggleLights() == 0);
    // Turn lights on one more time
    REQUIRE(testObj.toggleLights() == 1);
}

/*
 * Test station announcements
 */
TEST_CASE( "Test announceStations", "[Controller::announceStations()]")
{
    // Create new controller
    Controller testObj;
    // Turn announcements on
    REQUIRE(testObj.announceStations() == 1);
    // Turn announcements off
    REQUIRE(testObj.announceStations() == 0);
    // Turn announcements on one more time
    REQUIRE(testObj.announceStations() == 1);
}

/*
 * Test advertisements toggle
 */
TEST_CASE( "Test toggleAds", "[Controller::toggleAds()]")
{
    // Create new controller
    Controller testObj;
    // Turn advertisements on
    REQUIRE(testObj.toggleAds() == 1);
    // Turn advertisements off
    REQUIRE(testObj.toggleAds() == 0);
    // Turn advertisements on one more time
    REQUIRE(testObj.toggleAds() == 1);
}

/*
 * Test air conditioning toggle
 */
TEST_CASE( "Test toggleAirConditioning", "[Controller::toggleAirConditioning()]")
{
    // Create new controller
    Controller testObj;
    // Turn air conditioning on
    REQUIRE(testObj.toggleAirConditioning() == 1);
    // Turn air conditioning off
    REQUIRE(testObj.toggleAirConditioning() == 0);
    // Turn air conditioning on one more time
    REQUIRE(testObj.toggleAirConditioning() == 1);
}