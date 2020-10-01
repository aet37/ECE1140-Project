/**
 * @file RequestManager.cpp
 * 
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "RequestManager.hpp" // Header for class
#include "Request.hpp" // For Request
#include "Response.hpp" // For Response

namespace HWTrackController
{

// Static members
std::queue<Request*> RequestManager::m_requestQueue = std::queue<Request*>();
std::queue<Response*> RequestManager::m_responseQueue = std::queue<Response*>();

void RequestManager::AddRequest(Request& rReq)
{
    Request* pNewRequest = new Request();
    *(pNewRequest) = rReq;
    m_requestQueue.push(pNewRequest);
}

} // namespace HWTrackController