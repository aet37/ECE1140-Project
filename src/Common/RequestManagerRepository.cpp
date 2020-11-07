/**
 * @file RequestManagerRepository.cpp
 *
 * @brief Implementations of the RequestManagerRepository class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "RequestManagerRepository.hpp" // Header for class
#include "Assert.hpp" // For ASSERT
#include "RequestManagerIface.hpp" // For RequestManagerIface
#include "DebugRequestManager.hpp" // For Debug::DebugRequestManager
#include "HWTrackControllerRequestManager.hpp" // For HWTrackController::HWTrackControllerRequestManager
#include "CTCRequestManager.hpp"    // For CTC::CTCRequestManager
#include "TrainModelRequestManager.hpp" // For TrainModel::TrainModelRequestManager
#include "SWTrackControllerRequestManager.hpp" // For SWTrackController::SWTrackControllerRequestManager
#include "SWTrainControllerRequestManager.hpp" // For SWTrainController::SWTrainControllerRequestManager
#include "TrackModelRequestManager.hpp" // For TrackModel::TrackModelRequestManager

static Debug::DebugRequestManager debugRequestManager;
static CTC::CTCRequestManager ctcRequestManager;
static SWTrackController::SWTrackControllerRequestManager swTrackControllerRequestManager;
static HWTrackController::HWTrackControllerRequestManager hwTrackControllerRequestManager;
static TrackModel::TrackModelRequestManager trackModelRequestManager;
static TrainModel::TrainModelRequestManager trainModelRequestManager;
static SWTrainController::SWTrainControllerRequestManager swTrainControllerRequestManager;

namespace Common
{

RequestManagerIface* RequestManagerRepository::GetRequestManager(RequestCode requestCode)
{
    RequestManagerIface* pRequestManager = nullptr;

    // Convert to an integer to check whose request manager to return
    uint8_t requestCodeValue = static_cast<uint8_t>(requestCode);

    if (requestCodeValue <= 31)
    {
        pRequestManager = &debugRequestManager;
    }
    else if (requestCodeValue <= 63)
    {
        pRequestManager = &ctcRequestManager;
    }
    else if (requestCodeValue <= 95)
    {
        pRequestManager = &swTrackControllerRequestManager;
    }
    else if (requestCodeValue <= 127)
    {
        pRequestManager = &hwTrackControllerRequestManager;
    }
    else if (requestCodeValue <= 159)
    {
        pRequestManager = &trackModelRequestManager;
    }
    else if (requestCodeValue <= 191)
    {
        pRequestManager = &trainModelRequestManager;
    }
    else if (requestCodeValue <= 223)
    {
        pRequestManager = &swTrainControllerRequestManager;
    }
    else
    {
        // pRequestManager = &hwTrainControllerRequestManager;
    }

    ASSERT(pRequestManager != nullptr, "No request manager found for code %d", requestCode);

    return pRequestManager;
}

} // namespace Common
