/**
 * @file HWTrackCtrlTestSuite.cpp
*/
#define CATCH_CONFIG_RUNNER

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch_session.hpp>

int main(int argc, char* argv[])
{
    // Global setup
    // (None)

    int result = Catch::Session().run(argc, argv);

    return result;
}
