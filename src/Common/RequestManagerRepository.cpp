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

static Debug::DebugRequestManager debugRequestManager;
static HWTrackController::HWTrackControllerRequestManager hwTrackControllerRequestManager;
static CTC::CTCRequestManager ctcRequestManager;
static TrainModel::TrainModelRequestManager trainModelRequestManager;

namespace Common
{

RequestManagerIface* RequestManagerRepository::GetRequestManager(RequestCode requestCode)
{
    RequestManagerIface* pRequestManager = nullptr;

    switch (requestCode)
    {
        case RequestCode::DEBUG_TO_CTC:
        case RequestCode::DEBUG_TO_HWTRACKCTRL:
        case RequestCode::DEBUG_TO_SWTRACKCTRL:
        case RequestCode::DEBUG_TO_TRACK_MODEL:
        case RequestCode::DEBUG_TO_TRAIN_MODEL:
        case RequestCode::DEBUG_TO_HWTRAINCTRL:
        case RequestCode::DEBUG_TO_SWTRAINCTRL:
            pRequestManager = &debugRequestManager;
            break;
    	case RequestCode::CTC_DISPATCH_TRAIN:
    	case RequestCode::CTC_SEND_GUI_OCCUPANCIES:
			pRequestManager = &ctcRequestManager;
    		break;
        case RequestCode::HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST:
        case RequestCode::HWTRACK_SEND_HW_TRACK_CONTROLLER_REQUEST:
        case RequestCode::HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE:
            pRequestManager = &hwTrackControllerRequestManager;
            break;

        case RequestCode::TRAIN_MODEL_GET_CURRENT_SPEED:
            pRequestManager = &trainModelRequestManager;
            break;
        default:
            break;
    }

    ASSERT(pRequestManager != nullptr, "requestCode %d not handled", requestCode);

    return pRequestManager;
}

} // namespace Common
