/**
 * @file RequestManager.cpp
 *
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrainControllerRequestManager.h" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros

namespace HWTrainController
{

// Static members
std::queue<Common::Request*> HWTrainControllerRequestManager::m_requestQueue = std::queue<Common::Request*>();
std::queue<Common::Response*> HWTrainControllerRequestManager::m_responseQueue = std::queue<Common::Response*>();

void HWTrainControllerRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::GET_AUTHORITY:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::SET_AUTHORITY:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }

        // DO REST OF RESPONSE CODES
        case Common::RequestCode::GET_HW_TRAIN_CONTROLLER_REQUEST:
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
        case Common::RequestCode::SEND_HW_TRAIN_CONTROLLER_RESPONSE:
        {
            // Construct a response from the request's data and add it to the queue
            Common::Response resp(Common::ResponseCode::SUCCESS, rRequest.GetData());
            AddResponse(resp);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        case Common::RequestCode::GET_HW_TRAIN_CONTROLLER_RESPONSE:
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
            LOG_HW_Train_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

void HWTrainControllerRequestManager::AddRequest(const Common::Request& rReq)
{
    // Use heap memory so it can stay in the queue
    Common::Request* pNewRequest = new Common::Request();
    *(pNewRequest) = rReq;
    m_requestQueue.push(pNewRequest);
}

Common::Request* HWTrainControllerRequestManager::GetNextRequest()
{
    Common::Request* pNextRequest = nullptr;
    if (m_requestQueue.empty() != true)
    {
        pNextRequest = m_requestQueue.front();
        m_requestQueue.pop();
    }
    return pNextRequest;
}

void HWTrainControllerRequestManager::AddResponse(const Common::Response& rResp)
{
    // Use heap memory so it can stay in the queue
    Common::Response* pNewResponse = new Common::Response();
    *(pNewResponse) = rResp;
    m_responseQueue.push(pNewResponse);
}

Common::Response* HWTrainControllerRequestManager::GetNextResponse()
{
    Common::Response* pNextResponse = nullptr;
    if (m_responseQueue.empty() != true)
    {
        pNextResponse = m_responseQueue.front();
        m_responseQueue.pop();
    }
    return pNextResponse;
}

} // namespace HWTrainController
