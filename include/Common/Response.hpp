/**
 * @file Response.hpp
 * 
 * @brief Data structure to be used to respond to a request
*/
#ifndef RESPONSE_HPP
#define RESPONSE_HPP

// SYSTEM INCLUDES
#include <stdint.h>

namespace Common
{

/**
 * @enum ResponseCode
 * 
 * @brief Codes that will be used when the server
 * response back from a request
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
enum class ResponseCode
{
    SUCCESS = 0,
    ERROR = 1,
    SWITCH_POSITION = 1
};

/// Maximum number of bytes that can be sent in a response
const uint16_t MAX_RESPONSE_DATA_LENGTH_IN_BYTES = 1023;

/**
 * @struct Response
 * 
 * @brief Structure used to hold the response code and
 * any additional information for the response
*/
typedef struct Response
{
    /// What the response is of
    ResponseCode respCode;

    /// Data to go along with response
    uint8_t pData[MAX_RESPONSE_DATA_LENGTH_IN_BYTES];
} Response;

} // namespace Common

#endif // RESPONSE_HPP
