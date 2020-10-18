/**
 * @file Communications.cpp
*/

// SYSTEM INCLUDES
#include <assert.h>
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/Communications.hpp" // Header for class
#include "../include/UserProgram.hpp" // For UserProgram
#include "../include/TagDatabase.hpp" // For TagDatabase
#include "../include/Logger.hpp"

namespace Communications
{

/**
 * @brief Parses the request message to determine the request code
 *
 * @param rMsg     Request string
 * @return request code of the message
*/
static RequestCode ParseCode(const String& rMsg)
{
    int spaceIndex = rMsg.indexOf(' ');
    int code;
    if (spaceIndex == -1)
    {
        code = atoi(rMsg.c_str());
    }
    else
    {
        String codeString = rMsg.substring(0, spaceIndex);
        code = atoi(codeString.c_str());
    }

    switch (code)
    {
        case static_cast<int>(RequestCode::GET_SWITCH_POSITION):
        case static_cast<int>(RequestCode::SET_SWITCH_POSITION):
            return static_cast<RequestCode>(code);
        default:
            return RequestCode::INVALID;
    }
}

/**
 * @brief Parses the data that follows the request code in the message
 *
 * @param rMsg      Request string
 * @return Data following ' ' in message
*/
static String ParseData(const String& rMsg)
{
    int spaceIndex = rMsg.indexOf(' ');
    if (spaceIndex == -1)
    {
        return "";
    }
    else
    {
        return rMsg.substring(spaceIndex + 1, rMsg.length());
    }
}

/**
 * @brief Constructs and writes a response to Serial
 *
 * @param respCode      Response code to send
 * @param pData         Additional data to respond with
*/
static void SendResponse(ResponseCode respCode, const char* pData = "")
{
    Serial.print(static_cast<int>(respCode), DEC);
    Serial.print(" ");
    Serial.println(pData);
}

/**
 * @brief Gets a specified tag's value and sends a response
*/
static void GetTagValue(const String& rData)
{
    bool tagValue;
    if (TagDatabase::GetTagValue(rData, tagValue))
    {
        SendResponse(ResponseCode::SUCCESS, tagValue ? "1" : "0");
    }
    else
    {
        SendResponse(ResponseCode::ERROR);
    }
}

/**
 * @brief Sets a specified tag's value and sends a response
*/
static void SetTagValue(const String& rData)
{
    // Parse the message between tag name and value
    String tagName = rData.substring(0, rData.indexOf(" "));
    bool value = atoi(rData.substring(rData.indexOf(" "), rData.length()).c_str());
    digitalWrite(LED_BUILTIN, value ? HIGH : LOW);

    // Set the tags value and send the response
    bool ret = TagDatabase::SetTag(tagName, value);
    SendResponse(static_cast<ResponseCode>(!ret));
}

void CommsTask(void* pProgram)
{
    // Quickly return if nothing has been received
    if (Serial.available() == 0)
    {
        return;
    }

    // Read the message and determine the request code
    String msg = Serial.readStringUntil('\n');
    RequestCode code = ParseCode(msg);
    String data = ParseData(msg);

    switch (code)
    {
        case RequestCode::INVALID:
            SendResponse(ResponseCode::ERROR);
            break;
        case RequestCode::GET_SWITCH_POSITION:
            GetTagValue(data);
            break;
        case RequestCode::SET_SWITCH_POSITION:
            SetTagValue(data);
            break;
        default:
            // We expect ParseCode to take care of this case
            assert(false);
    }
}

} // namespace Communications
