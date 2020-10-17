/**
 * @file RequestManager.cpp
 *
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrackControllerRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros

namespace HWTrackController
{

// Static members
Common::ServiceQueue<Common::Request*> HWTrackControllerRequestManager::m_requestQueue = Common::ServiceQueue<Common::Request*>();
Common::ServiceQueue<Common::Response*> HWTrackControllerRequestManager::m_responseQueue = Common::ServiceQueue<Common::Response*>();

void HWTrackControllerRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::GET_SWITCH_POSITION:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SET_SWITCH_POSITION:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::GET_HW_TRACK_CONTROLLER_REQUEST:
        {
            // Retrieve the next request from the request queue
            Common::Request* pNextRequest = GetNextRequest();
            if (pNextRequest != nullptr)
            {
                rResponse.SetResponseCode(static_cast<Common::ResponseCode>(pNextRequest->GetRequestCode()));
                rResponse.SetData(pNextRequest->GetData());
                delete pNextRequest;
            }
            else
            {
                // Respond with error if there is none
                rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            }
            break;
        }
        case Common::RequestCode::SEND_HW_TRACK_CONTROLLER_RESPONSE:
        {
            // Construct a response from the request's data and add it to the queue
            Common::Response resp(Common::ResponseCode::SUCCESS, rRequest.GetData());
            AddResponse(resp);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::GET_HW_TRACK_CONTROLLER_RESPONSE:
        {
            // Retrieve a response from the queue
            Common::Response* pNextResponse = GetNextResponse();
            if (pNextResponse != nullptr)
            {
                rResponse = *(pNextResponse);
                delete pNextResponse;
            }
            else
            {
                // Respond with error if there are none
                rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            }
            break;
        }
        default:
            LOG_HW_TRACK_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

void HWTrackControllerRequestManager::AddRequest(const Common::Request& rReq)
{
    // Use heap memory so it can stay in the queue
    Common::Request* pNewRequest = new Common::Request();
    *(pNewRequest) = rReq;
    m_requestQueue.push(pNewRequest);
}

Common::Request* HWTrackControllerRequestManager::GetNextRequest()
{
    Common::Request* pNextRequest = nullptr;
    if (m_requestQueue.empty() != true)
    {
        pNextRequest = m_requestQueue.front();
        m_requestQueue.pop();
    }
    return pNextRequest;
}

void HWTrackControllerRequestManager::AddResponse(const Common::Response& rResp)
{
    // Use heap memory so it can stay in the queue
    Common::Response* pNewResponse = new Common::Response();
    *(pNewResponse) = rResp;
    m_responseQueue.push(pNewResponse);
}

Common::Response* HWTrackControllerRequestManager::GetNextResponse()
{
    Common::Response* pNextResponse = nullptr;
    if (m_responseQueue.empty() != true)
    {
        pNextResponse = m_responseQueue.front();
        m_responseQueue.pop();
    }
    return pNextResponse;
}

} // namespace HWTrackController
