/**
 * @file RequestManagerIface.hpp
*/
#ifndef REQUEST_MANAGER_BASE_HPP
#define REQUEST_MANAGER_BASE_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

// FORWARD REFERENCES
class Request;
class Response;

namespace Common
{

/**
 * @class RequestManagerIface
 *
 * @brief Interface for request managers. This will
 * be used by the RequestManagerRepository
*/
class RequestManagerIface
{
public:
    /**
     * @brief Virtual method for subclass to define.
    */
    virtual void HandleRequest(Request& rRequest, Response& rResp) = 0;

    /**
     * @brief Destroys the RequestManagerIface object
    */
    ~RequestManagerIface() {}

protected:
private:
};

} // namespace Common

#endif // REQUEST_MANAGER_BASE_HPP