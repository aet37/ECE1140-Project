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

    SET_SWITCH_POSITION = 96,
    GET_SWITCH_POSITION = 97
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
