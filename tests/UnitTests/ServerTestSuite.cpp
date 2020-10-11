/**
 * @file ServerTestSuite.cpp
*/
#define CATCH_CONFIG_RUNNER

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch.hpp>

int main(int argc, char* argv[])
{
    // Global setup

    int result = Catch::Session().run( argc, argv );

    return result;
}