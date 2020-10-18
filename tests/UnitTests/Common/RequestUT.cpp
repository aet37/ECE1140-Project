/**
 * @file RequestUT.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch_all.hpp>
#include "Request.hpp" // UUT

TEST_CASE("ParseData")
{
    Common::Request req(Common::RequestCode::DEBUG_TO_CTC, "32 15 632 8 switch");

    REQUIRE(Common::RequestCode::DEBUG_TO_CTC == req.GetRequestCode());
    REQUIRE("32 15 632 8 switch" == req.GetData());

    REQUIRE(32 == req.ParseData<uint32_t>(0));
    REQUIRE(15 == req.ParseData<uint32_t>(1));
    REQUIRE(632 == req.ParseData<uint32_t>(2));
    REQUIRE(8 == req.ParseData<uint32_t>(3));
    REQUIRE("switch" == req.ParseData<std::string>(4));
    REQUIRE_THROWS(req.ParseData<uint32_t>(5));
}

TEST_CASE("AppendData")
{
    Common::Request req;

    req.SetRequestCode(Common::RequestCode::DEBUG_TO_CTC);
    req.AppendData("542");
    req.AppendData("89");
    req.AppendData("switch1");

    REQUIRE("542 89 switch1" == req.GetData());
}
