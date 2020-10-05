/**
 * @file Communications.cpp
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/Communications.hpp" // Header for class

namespace Communications
{

/**
 * 
*/
static RequestCode DetermineCode(String& rData)
{
    int spaceIndex = rData.indexOf(' ');
    String codeString = rData.substring(0, spaceIndex);
    int code = atoi(codeString.c_str());

    switch (code)
    {
        case static_cast<int>(RequestCode::GET_SWITCH_POSITION):
        case static_cast<int>(RequestCode::SET_SWITCH_POSITION):
            return static_cast<RequestCode>(code);
        default:
            return RequestCode::INVALID;
    }
}

void CommsTask(void* something)
{
    // Quickly return if nothing has been received
    if (Serial.available() == 0)
    {
        return;
    }

    String data = Serial.readStringUntil('\n');
    RequestCode code = DetermineCode(data);
}

} // namespace Communications
