/**
 * @file Request.hpp
 * 
 * @brief Data structure to be used to request an action of a module
*/
#ifndef REQUEST_HPP
#define REQUEST_HPP

// SYSTEM INCLUDES
#include <stdint.h>

enum RequestCode
{
    ERROR = 0,
    SET_SWITCH_POSITION = 1,
    GET_SWITCH_POSITION = 2,
    GET_HW_TRACK_CONTROLLER_REQUEST = 3
};

const uint16_t MAX_REQUEST_DATA_LENGTH = 1024;

typedef struct Request
{
    /// What the request is for
    RequestCode reqCode;

    /// Data to go along with request
    uint8_t pData[MAX_REQUEST_DATA_LENGTH];
} Request;

#endif // REQUEST_HPP
