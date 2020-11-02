/**
 * @file Communications.hpp
*/
#ifndef COMMUNICATIONS_HPP
#define COMMUNICATIONS_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

namespace Communications
{

/**
 * @enum RequestCode
*/
enum class RequestCode
{
    INVALID = 1,
    CHECK = 2,

    HWTRACK_START_DOWNLOAD = 96,
    HWTRACK_END_DOWNLOAD = 97,
    HWTRACK_CREATE_TAG = 98,
    HWTRACK_CREATE_TASK = 99,
    HWTRACK_CREATE_ROUTINE = 100,
    HWTRACK_CREATE_RUNG = 101,
    HWTRACK_SET_TAG_VALUE = 102,
    HWTRACK_GET_TAG_VALUE = 103
};

/**
 * @enum ResponseCode
*/
enum class ResponseCode
{
    SUCCESS = 0,
    ERROR = 1,
};

/**
 * @brief Main function to run to handle communications
 * with the connected computer, server, and user interface
*/
void CommsTask(void* pProgram);

} // namespace Communications

#endif // COMMUNICATIONS_HPP
