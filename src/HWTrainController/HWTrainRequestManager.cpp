#include "HWTrainRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros


namespace HWTrainController
{

// Static members
Common::ServiceQueue<Common::Request*> HWTrainRequestManager::m_requestQueue;
Common::ServiceQueue<Common::Response*> HWTrainRequestManager::m_responseQueue;

void HWTrainRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::HWTRAIN_PULL_EBRAKE:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_SET_SETPOINT_SPEED:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_PRESS_SERVICE_BRAKE:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_TOGGLE_DAMN_DOORS:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_TOGGLE_CABIN_LIGHTS:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_SET_TEMPERATURE:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_ANNOUNCE_STATIONS:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_DISPLAY_ADS:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_DISPATCH_TRAIN:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST:
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
        case Common::RequestCode::HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE:
        {
            // Construct a response from the request's data and add it to the queue
            Common::Response resp(Common::ResponseCode::SUCCESS, rRequest.GetData());
            AddResponse(resp);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE:
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
        case Common::RequestCode::HWTRAIN_DISPATCH_TRAIN:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        default:
            LOG_HW_TRACK_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

void HWTrainRequestManager::AddRequest(const Common::Request& rReq)
{
    // Use heap memory so it can stay in the queue
    Common::Request* pNewRequest = new Common::Request();
    *(pNewRequest) = rReq;
    m_requestQueue.Push(pNewRequest);
}

Common::Request* HWTrainRequestManager::GetNextRequest()
{
    Common::Request* pNextRequest = nullptr;
    if (m_requestQueue.IsEmpty() != true)
    {
        pNextRequest = m_requestQueue.Pop();
    }
    return pNextRequest;
}

void HWTrainRequestManager::AddResponse(const Common::Response& rResp)
{
    // Use heap memory so it can stay in the queue
    Common::Response* pNewResponse = new Common::Response();
    *(pNewResponse) = rResp;
    m_responseQueue.Push(pNewResponse);
}

Common::Response* HWTrainRequestManager::GetNextResponse()
{
    Common::Response* pNextResponse = nullptr;
    if (m_responseQueue.IsEmpty() != true)
    {
        pNextResponse = m_responseQueue.Pop();
    }
    return pNextResponse;
}

} // namespace HWTrainController
