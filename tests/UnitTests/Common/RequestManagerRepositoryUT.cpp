/**
 * @file RequestManagerRepositoryUT.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators_all.hpp>
#include "RequestManagerRepository.hpp" // UUT
#include "DebugRequestManager.hpp"
#include "CTCRequestManager.hpp"
#include "SWTrackControllerRequestManager.hpp"
#include "HWTrackControllerRequestManager.hpp"
#include "TrackModelRequestManager.hpp"
#include "TrainModelRequestManager.hpp"
#include "SWTrainControllerRequestManager.hpp"
// #include "HWTrainControllerRequestManager.hpp"
#include "Request.hpp"

TEST_CASE("Singleton")
{
    Common::RequestManagerRepository& repo = Common::RequestManagerRepository::GetInstance();
    REQUIRE(&Common::RequestManagerRepository::GetInstance() == &repo);
}

TEST_CASE("Debug request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(0, 31)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<Debug::DebugRequestManager*>(pReqManager));
}

TEST_CASE("CTC request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(32, 63)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<CTC::CTCRequestManager*>(pReqManager));
}

TEST_CASE("SWTrackController request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(64, 95)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<SWTrackController::SWTrackControllerRequestManager*>(pReqManager));
}

TEST_CASE("HWTrackController request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(96, 127)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<HWTrackController::HWTrackControllerRequestManager*>(pReqManager));
}

TEST_CASE("TrackModel request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(128, 159)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<TrackModel::TrackModelRequestManager*>(pReqManager));
}

TEST_CASE("TrainModel request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(160, 191)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<TrainModel::TrainModelRequestManager*>(pReqManager));
}

TEST_CASE("SWTrainController request managers")
{
    Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(192, 223)));
    Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
    REQUIRE(nullptr != dynamic_cast<SWTrainController::SWTrainControllerRequestManager*>(pReqManager));
}

// TEST_CASE("HWTrainController request managers")
// {
//     Common::RequestCode reqCode = static_cast<Common::RequestCode>(GENERATE(range(224, 255)));
//     Common::RequestManagerIface* pReqManager = Common::RequestManagerRepository::GetInstance().GetRequestManager(reqCode);
//     REQUIRE(nullptr != dynamic_cast<HWTrainController::HWTrainControllerRequestManager*>(pReqManager));
// }
