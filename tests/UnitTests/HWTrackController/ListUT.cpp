/**
 * @file ListUT.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch_test_macros.hpp>
#include "List.hpp" // UUT

TEST_CASE("Basic functionality")
{
    List<uint32_t> list(10);

    for (uint32_t i = 0; i < 15; i++)
    {
        list.Append(i);
    }

    for (uint32_t i = 0; i < 15; i++)
    {
        REQUIRE(list[i] == i);
    }

    REQUIRE(list.GetLength() == 15);
    REQUIRE_FALSE(list.IsEmpty());

    list[0] = 100;
    REQUIRE(list[0] == 100);
}
