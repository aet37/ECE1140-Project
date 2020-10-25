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
<<<<<<< HEAD
#include "HWTrainRequestManager.hpp"
=======
//#include "SWTrackControllerRequestManager.hpp"
#include "TrackModelRequestManager.hpp" // For TrackModel::TrackModelRequestManager
>>>>>>> origin/master

static Debug::DebugRequestManager debugRequestManager;
static HWTrackController::HWTrackControllerRequestManager hwTrackControllerRequestManager;
static CTC::CTCRequestManager ctcRequestManager;
static TrainModel::TrainModelRequestManager trainModelRequestManager;
<<<<<<< HEAD
static HWTrainController::HWTrainRequestManager hwTrainControllerRequestManager;

=======
static TrackModel::TrackModelRequestManager trackModelRequestManager;
//static SWTrackController::SWTrackControllerRequestManager swTrackControllerRequestManager;
>>>>>>> origin/master
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

        case RequestCode::TRAIN_MODEL_DISPATCH_TRAIN:
            pRequestManager = &trainModelRequestManager;
            break;
<<<<<<< HEAD
        case RequestCode::HWTRAIN_PULL_EBRAKE:
        case RequestCode::HWTRAIN_SET_SETPOINT_SPEED:
        case RequestCode::HWTRAIN_PRESS_SERVICE_BRAKE:
        case RequestCode::HWTRAIN_TOGGLE_DAMN_DOORS:
        case RequestCode::HWTRAIN_TOGGLE_CABIN_LIGHTS:
        case RequestCode::HWTRAIN_SET_TEMPERATURE:
        case RequestCode::HWTRAIN_ANNOUNCE_STATIONS:
        case RequestCode::HWTRAIN_DISPLAY_ADS:
        case RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST:
        case RequestCode::HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE:
        case RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE:
            pRequestManager = &hwTrainControllerRequestManager;
            break;
=======

        case RequestCode::TRACK_MODEL_DISPATCH_TRAIN:
            pRequestManager = &trackModelRequestManager;
            break;
            
>>>>>>> origin/master
        default:
            break;
    }

    ASSERT(pRequestManager != nullptr, "No request manager found for code %d", requestCode);

    return pRequestManager;
}

} // namespace Common
