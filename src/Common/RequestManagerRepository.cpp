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

static HWTrackController::HWTrackControllerRequestManager hwTrackControllerRequestManager;
static CTC::CTCRequestManager ctcRequestManager;

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

        default:
            break;
    }

    ASSERT(pRequestManager != nullptr, "requestCode %d not handled", requestCode);

    return pRequestManager;
}

} // namespace Common
