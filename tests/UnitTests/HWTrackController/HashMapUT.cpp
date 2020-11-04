/**
 * @file HashMapUT.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch_test_macros.hpp>
#include "HashMap.hpp" // UUT

TEST_CASE("HashMap Basic Functionality")
{
    std::string keys[] = {"ABC", "DEF", "GHI", "JKL", "MNOP", "QRS", "TUV", "WX", "YZ"};
    HashMap<uint32_t> hashMap = HashMap<uint32_t>(5);

    for (uint32_t i = 0; i < 9; i++)
    {
        hashMap.Insert(keys[i], i);
    }

    SECTION("Get")
    {
        for (uint32_t i = 0; i < 9; i++)
        {
            REQUIRE(hashMap.Get(keys[i]) == i);
        }
    }

    SECTION("Contains")
    {
        REQUIRE(hashMap.Contains("ABC"));
        REQUIRE_FALSE(hashMap.Contains("BADKEY"));
    }

    SECTION("Update")
    {
        hashMap.Update("ABC", 100);
        REQUIRE(100 == hashMap.Get("ABC"));

        REQUIRE_FALSE(hashMap.Update("XYZ", 50));
    }

    SECTION("Clear")
    {
        hashMap.Clear();

        for (uint32_t i = 0; i < 9; i++)
        {
            REQUIRE_FALSE(hashMap.Contains(keys[i]));
        }
    }
}
