/**
 * @file RequestManager.cpp
 * 
 * @brief Implementation of RequestManager class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "RequestManager.hpp"

// Static members
std::queue<RequestManager::Request*> RequestManager::m_requestQueue = std::queue<Request*>();
std::queue<RequestManager::Response*> RequestManager::m_responseQueue = std::queue<Response*>();