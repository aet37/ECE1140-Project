/**
 * @file RequestManager.cpp
 * 
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
#include <iostream> // For std::cout

// C++ PROJECT INCLUDES
#include "RequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response

namespace HWTrackController
{

// Static members
std::queue<Common::Request*> RequestManager::m_requestQueue = std::queue<Common::Request*>();
std::queue<Common::Response*> RequestManager::m_responseQueue = std::queue<Common::Response*>();

void RequestManager::HandleRequest(Common::Request& rRequest, Common::Response& rResponse)
{
    switch (rRequest.GetRequestCode())
    {
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
                rResponse.SetResponseCode(Common::ResponseCode::SUCCESS);
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
            Common::Response resp(static_cast<Common::ResponseCode>(std::stoi(rRequest.GetData())));
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
            std::cerr << "Invalid command " << static_cast<uint16_t>(rRequest.GetRequestCode())
                      << " received" << std::endl;
            rResponse.SetData("INVALID COMMAND");
            return;
    }
}

void RequestManager::AddRequest(Common::Request& rReq)
{
    // Use heap memory so it can stay in the queue
    Common::Request* pNewRequest = new Common::Request();
    *(pNewRequest) = rReq;
    m_requestQueue.push(pNewRequest);
}

Common::Request* RequestManager::GetNextRequest()
{
    Common::Request* pNextRequest = nullptr;
    if (m_requestQueue.empty() != true)
    {
        pNextRequest = m_requestQueue.front();
        m_requestQueue.pop();
    }
    return pNextRequest;
}

void RequestManager::AddResponse(Common::Response& rResp)
{
    // Use heap memory so it can stay in the queue
    Common::Response* pNewResponse = new Common::Response();
    *(pNewResponse) = rResp;
    m_responseQueue.push(pNewResponse);
}

Common::Response* RequestManager::GetNextResponse()
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
