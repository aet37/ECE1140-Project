/**
 * @file Request.hpp
 * 
 * @brief Data structure to be used to request an action of a module
*/
#ifndef REQUEST_HPP
#define REQUEST_HPP

// SYSTEM INCLUDES
#include <stdint.h>

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
    ERROR = 0,
    SET_SWITCH_POSITION = 1,
    GET_SWITCH_POSITION = 2,
    GET_HW_TRACK_CONTROLLER_REQUEST = 3
};

/// Maximum number of bytes of data in a request.
const uint16_t MAX_REQUEST_DATA_LENGTH_IN_BYTES = 1023;

/**
 * @struct Request
 * 
 * @brief Structure used to hold the request code and
 * additional data
*/
typedef struct Request
{
    /// What the request is for
    RequestCode reqCode;

    /// Data to go along with request
    uint8_t pData[MAX_REQUEST_DATA_LENGTH_IN_BYTES];
} Request;

} // namespace Common

#endif // REQUEST_HPP
