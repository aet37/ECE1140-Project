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
#include "../include/Task.hpp" // For Task
#include "../include/ArduinoLogger.hpp" // For LOG macros

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
        case static_cast<int>(RequestCode::HWTRACK_START_DOWNLOAD):
        case static_cast<int>(RequestCode::HWTRACK_CREATE_TASK):
        case static_cast<int>(RequestCode::HWTRACK_END_DOWNLOAD):
        case static_cast<int>(RequestCode::HWTRACK_GET_TAG_VALUE):
        case static_cast<int>(RequestCode::HWTRACK_SET_TAG_VALUE):
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
 * @brief Deletes the current program and starts a new one with the given name
 *
 * @param pProgram      Pointer to the current program
 * @param rProgramName  Name of the new program
*/
static void HandleStartDownload(UserProgram* pProgram, const String& rProgramName)
{
    delete pProgram;
    pProgram = new UserProgram(rProgramName.c_str());
    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Creates a task given the parameters
 *
 * @param pProgram      Program that's being downloaded
 * @param rData         Parameters of the task in format: (PERIOD period | EVENT event) taskName
*/
static void HandleCreateTask(UserProgram* pProgram, const String& rData)
{
    // Pointer to the task that will be created
    Task* pTask;
    TaskType taskType = TaskType::PERIODIC;
    uint32_t periodInMs = 0;

    // Parse out task type and period or event
    int firstSpaceIndex = 0;
    int secondSpaceIndex = rData.indexOf(' ');
    String type = rData.substring(firstSpaceIndex, secondSpaceIndex);

    firstSpaceIndex = secondSpaceIndex;
    secondSpaceIndex = rData.indexOf(' ', firstSpaceIndex + 1);
    if (type.equals("PERIOD"))
    {
        String periodAsString = rData.substring(firstSpaceIndex + 1, secondSpaceIndex);
        periodInMs = periodAsString.toInt();
    }
    else if (type.equals("EVENT"))
    {
        taskType = TaskType::EVENT_DRIVEN;
        String eventName = rData.substring(firstSpaceIndex + 1, secondSpaceIndex);
        // TODO: Need to do something with this
    }
    else
    {
        SendResponse(ResponseCode::ERROR);
        return;
    }

    // Get the task name
    String taskName = rData.substring(secondSpaceIndex + 1);

    // Create task using parameters
    pTask = new Task(taskName.c_str(), taskType, periodInMs);

    // Add it to the program
    pProgram->AddTask(pTask);

    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Finishes a download by starting each periodic task
 *
 * @param pProgram      Program that has been downloaded
*/
static void HandleEndDownload(UserProgram* pProgram)
{
    SendResponse(ResponseCode::SUCCESS);
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
    UserProgram* pUserProgram = static_cast<UserProgram*>(pProgram);

    switch (code)
    {
        case RequestCode::INVALID:
            SendResponse(ResponseCode::ERROR);
            break;
        case RequestCode::CHECK:
            SendResponse(ResponseCode::SUCCESS);
            break;
        case RequestCode::HWTRACK_START_DOWNLOAD:
            HandleStartDownload(pUserProgram, data);
            break;
        case RequestCode::HWTRACK_CREATE_TASK:
            HandleCreateTask(pUserProgram, data);
            break;
        case RequestCode::HWTRACK_END_DOWNLOAD:
            HandleEndDownload(pUserProgram);
        case RequestCode::HWTRACK_GET_TAG_VALUE:
            GetTagValue(data);
            break;
        case RequestCode::HWTRACK_SET_TAG_VALUE:
            SetTagValue(data);
            break;
        default:
            // We expect ParseCode to take care of this case
            assert(false);
    }
}

} // namespace Communications
