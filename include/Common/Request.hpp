/**
 * @file Request.hpp
 * 
 * @brief Data structure to be used to request an action of a module
*/
#ifndef REQUEST_HPP
#define REQUEST_HPP

// SYSTEM INCLUDES
#include <stdint.h>
#include <string>

namespace Common
{

/**
 * @enum RequestCode
 * 
 * @brief Codes that will be used when communicating with
 * the server. Each module is assigned a range of numbers
 * 
 * @li System wide: 0 - 31
 * @li CTC: 32 - 63
 * @li Software Track Controller: 64 - 95
 * @li Hardware Track Controller: 96 - 127
 * @li Track Model: 128 - 159
 * @li Train Model: 160 - 191
 * @li Software Train Controller: 192 - 223
 * @li Hardware Train Controller: 224 - 255
*/
enum class RequestCode : uint8_t
{
    ERROR = 1,
    LOGIN = 2,

    SET_SWITCH_POSITION = 96,
    GET_SWITCH_POSITION = 97,
    GET_HW_TRACK_CONTROLLER_REQUEST = 100,
    SEND_HW_TRACK_CONTROLLER_RESPONSE = 101,
    GET_HW_TRACK_CONTROLLER_RESPONSE = 102
};

/**
 * @class Request
 * 
 * @brief Structure used to hold the request code and
 * additional data
*/
class Request
{
public:
    /**
     * @brief Constructs a new Request object
    */
    Request(RequestCode reqCode, std::string data) :
        m_reqCode(reqCode),
        m_data(data)
    {}

    Request() { Request(RequestCode::ERROR, ""); }
    explicit Request(RequestCode reqCode) { Request(reqCode, ""); }

    /**
     * @brief Sets the response code member
    */
    void SetRequestCode(const RequestCode reqCode) { m_reqCode = reqCode; }

    /**
     * @brief Sets the data string member
    */
    void SetData(const std::string data) { m_data = data; }

    /**
     * @brief Gets the data member
    */
    const std::string& GetData() const { return m_data; }

    /**
     * @brief Gets the request code member
    */
    RequestCode GetRequestCode() const { return m_reqCode; }

protected:
private:
    /// Request code to designate what the request is for
    RequestCode m_reqCode;

    /// Data to go along with request
    std::string m_data;
};

} // namespace Common

#endif // REQUEST_HPP
