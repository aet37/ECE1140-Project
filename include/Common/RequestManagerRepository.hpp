/**
 * @file RequestManagerRepository.hpp
 * 
 * @brief Declaration of the RequestManagerRepository class
*/
#ifndef REQUEST_MANAGER_REPOSITORY_HPP
#define REQUEST_MANAGER_REPOSITORY_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Request.hpp"

// FORWARD REFERENCES
class RequestManagerIface;

namespace Common
{

/**
 * @class RequestManagerRepository
 * 
 * @brief Repository for module's request managers
*/
class RequestManagerRepository
{
public:
    /**
     * @brief Gets the singleton instance
    */
    static RequestManagerRepository& GetInstance()
    {
        static RequestManagerRepository* pInstance = new RequestManagerRepository();
        return *(pInstance);
    }

    /**
     * @brief Retrieves a specific's module's request manager based
     * on the given request code
     * 
     * @param requestCode       Code of the request
     * @return Specific request manager to handle the request
    */
    RequestManagerIface* GetRequestManager(RequestCode requestCode);
protected:
private:
    /**
     * @brief Constructs a new RequestManagerRepository object
     * 
     * @note Private to ensure singleton instance
    */
    RequestManagerRepository() {}
};

} // namespace Common

#endif // REQUEST_MANAGER_REPOSITORY_HPP