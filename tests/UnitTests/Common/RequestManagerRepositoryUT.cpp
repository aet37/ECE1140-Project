/**
 * @file RequestManagerRepositoryUT.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch.hpp>
#include "RequestManagerRepository.hpp" // UUT
#include "HWTrackControllerRequestManager.hpp" // For HWTrackController::HWTrackControllerRequestManager
#include "Request.hpp"

TEST_CASE("Singleton")
{
    Common::RequestManagerRepository& repo = Common::RequestManagerRepository::GetInstance();
    REQUIRE(&Common::RequestManagerRepository::GetInstance() == &repo);
}

TEST_CASE("HWTrackController request managers")
{
    Common::RequestCode reqCode = GENERATE(Common::RequestCode::GET_HW_TRACK_CONTROLLER_REQUEST, 
                                           Common::RequestCode::SEND_HW_TRACK_CONTROLLER_RESPONSE,
                                           Common::RequestCode::GET_HW_TRACK_CONTROLLER_RESPONSE);
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<HWTrackController::HWTrackControllerRequestManager*>(pReqManager));
}