/**
 * @file CTCDefUT.cpp
*/

// SYSTEM INCLUDES
#include "CTCDef.hpp"

// C++ PROJECT INCLUDES
#include <catch2/catch_all.hpp>

/*
 * Test Train Struct Constructor
 */
TEST_CASE( "Test Train Struct Constructor", "[Train::Train()]" )
{
	Train ta1(3, 10);

	REQUIRE(ta1.train_id == 3);
	REQUIRE(ta1.destination_block == 10);
}

/*
 * Test Track Struct Constructor
 */
TEST_CASE( "Test Track Struct Constructor", "[Track::Track()]" )
{
	Track tr1;

	REQUIRE(tr1.open);  // Track initialized to open
	REQUIRE(!tr1.occupied);  // Track initialized to
}

TEST_CASE( "Test Signal Struct Constructor", "[Signal::Signal()]" )
{
	Signal s1;

	REQUIRE(s1.status == LIGHT_RED);
	REQUIRE(s1.track_on == nullptr);
}
