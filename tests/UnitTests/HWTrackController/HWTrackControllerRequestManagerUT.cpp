/**
 * @file HWTrackControllerRequestManagerUT.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch_test_macros.hpp>
#include "HWTrackControllerRequestManager.hpp" // UUT
#include "Request.hpp"
#include "Response.hpp"

TEST_CASE("Handle Request")
{
    HWTrackController::HWTrackControllerRequestManager rm;
    Common::Request req(Common::RequestCode::GET_SWITCH_POSITION);
    Common::Response resp;

    // Call method
    rm.HandleRequest(req, resp);

    REQUIRE(Common::ResponseCode::SUCCESS == resp.GetResponseCode());
}
