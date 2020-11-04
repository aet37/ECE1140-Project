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

TEST_CASE("Insertion")
{
    List<uint32_t> list(10);

    list.Append(1);
    list.Append(3);
    list.Append(5);
    list.Append(7);

    // Insert at the beginning
    list.Insert(0, 0);

    REQUIRE(list[0] == 0);
    REQUIRE(list[1] == 1);
    REQUIRE(list[2] == 3);
    REQUIRE(list[3] == 5);
    REQUIRE(list[4] == 7);

    // Insert at the end
    list.Insert(8, 5);

    REQUIRE(list[0] == 0);
    REQUIRE(list[1] == 1);
    REQUIRE(list[2] == 3);
    REQUIRE(list[3] == 5);
    REQUIRE(list[4] == 7);
    REQUIRE(list[5] == 8);

    // Insert in the middle
    list.Insert(4, 3);

    REQUIRE(list[0] == 0);
    REQUIRE(list[1] == 1);
    REQUIRE(list[2] == 3);
    REQUIRE(list[3] == 4);
    REQUIRE(list[4] == 5);
    REQUIRE(list[5] == 7);
    REQUIRE(list[6] == 8);
}
