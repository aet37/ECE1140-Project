/**
 * @file RequestManagerRepository.cpp
 * 
 * @brief Implementations of the RequestManagerRepository class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "RequestManagerRepository.hpp" // Header for class
#include "RequestManagerIface.hpp" // For RequestManagerIface

namespace Common
{

RequestManagerIface* RequestManagerRepository::GetRequestManager(RequestCode requestCode)
{
    RequestManagerIface* pRequestManager = nullptr;

    switch (requestCode)
    {

        default:
            break;
    }

    ASSERT(pRequestManager != nullptr, "requestCode %d not handled", requestCode);

    return pRequestManager;
}

} // namespace Common