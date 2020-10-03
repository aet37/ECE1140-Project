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
    switch(rRequest.reqCode)
    {
        case Common::RequestCode::SET_SWITCH_POSITION:
        {
            AddRequest(rRequest);
            rResponse.respCode = Common::ResponseCode::SUCCESS;
            break;
        }
        case Common::RequestCode::GET_HW_TRACK_CONTROLLER_REQUEST:
        {
            Common::Request* pNextRequest = GetNextRequest();
            if (pNextRequest != nullptr)
            {
                rResponse.respCode = Common::ResponseCode::SUCCESS;
                delete pNextRequest;
            }
            else
            {
                rResponse.respCode = Common::ResponseCode::ERROR;
            }
            break;
        }
        default:
            std::cerr << "Invalid command " << static_cast<uint16_t>(rRequest.reqCode) << " received" << std::endl;
            snprintf(reinterpret_cast<char*>(rResponse.pData), Common::MAX_RESPONSE_DATA_LENGTH_IN_BYTES, "INVALID COMMAND");
            return;
    }
}

void RequestManager::AddRequest(Common::Request& rReq)
{
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

} // namespace HWTrackController