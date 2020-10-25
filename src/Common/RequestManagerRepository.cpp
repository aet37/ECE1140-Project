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
#include "HWTrackControllerRequestManager.hpp" // For HWTrackController::HWTrackControllerRequestManager
#include "CTCRequestManager.hpp"    // For CTC::CTCRequestManager
#include "TrainModelRequestManager.hpp" // For TrainModel::TrainModelRequestManager
#include "SWTrackControllerRequestManager.hpp"

static HWTrackController::HWTrackControllerRequestManager hwTrackControllerRequestManager;
static CTC::CTCRequestManager ctcRequestManager;
static TrainModel::TrainModelRequestManager trainModelRequestManager;
static SWTrackController::SWTrackControllerRequestManager swTrackControllerRequestManager;

namespace Common
{

RequestManagerIface* RequestManagerRepository::GetRequestManager(RequestCode requestCode)
{
    RequestManagerIface* pRequestManager = nullptr;

    switch (requestCode)
    {
    	// To CTC
    	case RequestCode::CTC_DISPATCH_TRAIN:
    	case RequestCode::CTC_SEND_GUI_OCCUPANCIES:
			pRequestManager = &ctcRequestManager;
    		break;

    	// To HWTrackController
        case RequestCode::GET_HW_TRACK_CONTROLLER_REQUEST:
        case RequestCode::SEND_HW_TRACK_CONTROLLER_RESPONSE:
        case RequestCode::GET_HW_TRACK_CONTROLLER_RESPONSE:
            pRequestManager = &hwTrackControllerRequestManager;
            break;

        // To SWTrackController
        case RequestCode::SEND_TRACK_OCCUPANCY_TO_SW_TRACK_C:
            pRequestManager = &swTrackControllerRequestManager;
            break;
        default:
            break;
    }

    ASSERT(pRequestManager != nullptr, "No request manager found for code %d", requestCode);

    return pRequestManager;
}

} // namespace Common
