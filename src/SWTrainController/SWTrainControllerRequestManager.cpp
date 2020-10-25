/**
 * @file RequestManager.cpp
 *
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrainControllerRequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response
#include "Logger.hpp" // For LOG macros

namespace SWTrainController
{

// Static members
Common::ServiceQueue<Common::Request*> SWTrainControllerRequestManager::m_requestQueue;
Common::ServiceQueue<Common::Response*> SWTrainControllerRequestManager::m_responseQueue;

void SWTrainControllerRequestManager::HandleRequest(const Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
        case Common::RequestCode::SEND_TRAIN_MODEL_INFO:
        {
            // Add the request to the queue
            AddRequest(rRequest);
            rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
            break;
        }
        default:
            LOG_SW_TRAIN_CONTROLLER("Invalid command %d received", static_cast<uint16_t>(rRequest.GetRequestCode()));
            rResponse.SetResponseCode(Common::ResponseCode::ERROR);
            return;
    }
}

void SWTrainControllerRequestManager::AddRequest(const Common::Request& rReq)
{
    // Use heap memory so it can stay in the queue
    Common::Request* pNewRequest = new Common::Request();
    *(pNewRequest) = rReq;
    m_requestQueue.Push(pNewRequest);
}

Common::Request* SWTrainControllerRequestManager::GetNextRequest()
{
    Common::Request* pNextRequest = nullptr;
    if (m_requestQueue.IsEmpty() != true)
    {
        pNextRequest = m_requestQueue.Pop();
    }
    return pNextRequest;
}

void SWTrainControllerRequestManager::AddResponse(const Common::Response& rResp)
{
    // Use heap memory so it can stay in the queue
    Common::Response* pNewResponse = new Common::Response();
    *(pNewResponse) = rResp;
    m_responseQueue.Push(pNewResponse);
}

Common::Response* SWTrainControllerRequestManager::GetNextResponse()
{
    Common::Response* pNextResponse = nullptr;
    if (m_responseQueue.IsEmpty() != true)
    {
        pNextResponse = m_responseQueue.Pop();
    }
    return pNextResponse;
}

} // namespace SWTrainController
