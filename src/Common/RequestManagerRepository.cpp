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

#include "SWTrackControllerRequestManager.hpp" //For SWTrackController::SWTrackControllerRequestManager


#include "TrackModelRequestManager.hpp" // For TrackModel::TrackModelRequestManager


static Debug::DebugRequestManager debugRequestManager;
static HWTrackController::HWTrackControllerRequestManager hwTrackControllerRequestManager;
static CTC::CTCRequestManager ctcRequestManager;
static TrainModel::TrainModelRequestManager trainModelRequestManager;
static SW_TrackController::SWTrackControllerRequestManager swTrackControllerRequestManager;
static TrackModel::TrackModelRequestManager trackModelRequestManager;

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
    	case RequestCode::CTC_GUI_DISPATCH_TRAIN:
    	case RequestCode::CTC_SEND_GUI_OCCUPANCIES:
			pRequestManager = &ctcRequestManager;
    		break;
        case RequestCode::HWTRACK_GET_TAG_VALUE:
        case RequestCode::HWTRACK_SET_TAG_VALUE:
        case RequestCode::HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST:
        case RequestCode::HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE:
        case RequestCode::HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE:
            pRequestManager = &hwTrackControllerRequestManager;
            break;
        case RequestCode:: SWTRACK_DISPATCH_TRAIN:
        case RequestCode:: SWTRACK_UPDATE_AUTHORITY:
        case RequestCode:: SWTRACK_SET_TRACK_SIGNAL:
        case RequestCode:: SWTRACK_UPDATE_COMMAND_SPEED:
        case RequestCode:: SWTRACK_SET_TRACK_STATUS:
        case RequestCode:: SWTRACK_SET_SWITCH_POSITION:
        case RequestCode:: SWTRACK_SET_TRACK_FAILURE:
        case RequestCode:: SWTRACK_SET_TRACK_OCCUPANCY:
        case RequestCode:: SWTRACK_SET_CROSSING:
        case RequestCode:: SWTRACK_SET_TRACK_HEATER:  
            pRequestManager = &swTrackControllerRequestManager;
            break;

        case RequestCode::TRAIN_MODEL_DISPATCH_TRAIN:
            pRequestManager = &trainModelRequestManager;
            break;

        case RequestCode::TRACK_MODEL_DISPATCH_TRAIN:
            pRequestManager = &trackModelRequestManager;
            break;
            
        default:
            break;
    }

    ASSERT(pRequestManager != nullptr, "No request manager found for code %d", requestCode);

    return pRequestManager;
}

} // namespace Common
