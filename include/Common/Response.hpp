/**
 * @file Response.hpp
 * 
 * @brief Data structure to be used to respond to a request
*/
#ifndef RESPONSE_HPP
#define RESPONSE_HPP

// SYSTEM INCLUDES
#include <stdint.h>

enum ResponseCode
{
    STATUS = 0,
    SWITCH_POSITION = 1
};

const uint16_t MAX_RESPONSE_DATA_LENGTH = 1024;

typedef struct Response
{
    /// What the response is of
    ResponseCode respCode;

    /// Data to go along with response
    uint8_t pData[MAX_RESPONSE_DATA_LENGTH];
} Response;

#endif // RESPONSE_HPP
