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
#include "../include/Routine.hpp" // For Routine
#include "../include/Rung.hpp" // For Rung
#include "../include/Instruction.hpp" // For Instruction
#include "../include/Scheduler.hpp" // For Scheduler
#include "../include/Lcd/LcdApi.hpp" // For LcdApi
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
        case static_cast<int>(RequestCode::HWTRACK_CREATE_TAG):
        case static_cast<int>(RequestCode::HWTRACK_CREATE_TASK):
        case static_cast<int>(RequestCode::HWTRACK_CREATE_ROUTINE):
        case static_cast<int>(RequestCode::HWTRACK_CREATE_RUNG):
        case static_cast<int>(RequestCode::HWTRACK_CREATE_INSTRUCTION):
        case static_cast<int>(RequestCode::HWTRACK_END_DOWNLOAD):
        case static_cast<int>(RequestCode::HWTRACK_GET_TAG_VALUE):
        case static_cast<int>(RequestCode::HWTRACK_SET_TAG_VALUE):
        case static_cast<int>(RequestCode::HWTRACK_GET_ALL_TAG_VALUES):
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
    Scheduler::GetInstance().RemoveUserTasks();
    pProgram->ClearMemory();
    pProgram->SetProgramName(rProgramName.c_str());
    TagDatabase::Clear();
    LcdApi::Clear();
    LcdApi::Write("Download In Progress");
    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Creates a tag using the parameters provided
 *
 * @param rData     Name and default value of tag
*/
static void HandleCreateTag(const String& rData)
{
    int spaceIndex = rData.indexOf(' ');

    String tagName = rData.substring(0, spaceIndex);
    String defaultValue = rData.substring(spaceIndex + 1);

    if (defaultValue.equals("FALSE"))
    {
        TagDatabase::AddTag(tagName.c_str());
    }
    else if (defaultValue.equals("TRUE"))
    {
        TagDatabase::AddTag(tagName.c_str());
        TagDatabase::SetTag(tagName, true);
    }
    else
    {
        SendResponse(ResponseCode::ERROR);
        return;
    }

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
    String eventName;
    if (type.equals("PERIOD"))
    {
        String periodAsString = rData.substring(firstSpaceIndex + 1, secondSpaceIndex);
        periodInMs = periodAsString.toInt();
    }
    else if (type.equals("EVENT"))
    {
        taskType = TaskType::EVENT_DRIVEN;
        eventName = rData.substring(firstSpaceIndex + 1, secondSpaceIndex);
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

    // Set the event name if it's event driven
    if (taskType == TaskType::EVENT_DRIVEN)
    {
        pTask->SetEventName(eventName);
    }

    // Add it to the program
    pProgram->AddTask(pTask);

    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Creates a routine under the most recently created task
 *
 * @param pProgram  Program that's being downloaded
 * @param rData     Parameter of routine in format: (routineName)
*/
static void HandleCreateRoutine(UserProgram* pProgram, const String& rData)
{
    // Create the routine using the given name
    LOGN(rData);
    Routine* pRoutine = new Routine(rData.c_str());

    Task* pLastCreatedTask = pProgram->GetLastCreatedTask();
    if (rData.equals("Main"))
    {
        pLastCreatedTask->AddRoutine(pRoutine, true);
    }
    else
    {
        pLastCreatedTask->AddRoutine(pRoutine, false);
    }

    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Creates a rung under the most recently created routine
 *
 * @param pProgram  Program that's being downloaded
*/
static void HandleCreateRung(UserProgram* pProgram)
{
    Task* pTask = pProgram->GetLastCreatedTask();
    Routine* pRoutine = pTask->GetLastCreatedRoutine();

    pRoutine->AppendRung(new Rung());

    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Creates an instruction under the most recent rung
 * using the given parameters
*/
static void HandleCreateInstruction(UserProgram* pProgram, const String& rData)
{
    LOGN(rData);
    int spaceIndex = rData.indexOf(' ');
    String instType = rData.substring(0, spaceIndex);
    String arg = rData.substring(spaceIndex + 1);

    Instruction* pInstruction = nullptr;
    if (instType.equals("XIO"))
    {
        pInstruction = new Instruction(InstructionType::XIO, arg);
    }
    else if (instType.equals("XIC"))
    {
        pInstruction = new Instruction(InstructionType::XIC, arg);
    }
    else if (instType.equals("OTE"))
    {
        pInstruction = new Instruction(InstructionType::OTE, arg);
    }
    else if (instType.equals("OTL"))
    {
        pInstruction = new Instruction(InstructionType::OTL, arg);
    }
    else if (instType.equals("OTU"))
    {
        pInstruction = new Instruction(InstructionType::OTU, arg);
    }
    else if (instType.equals("JSR"))
    {
        pInstruction = new Instruction(InstructionType::JSR, arg);
    }
    else if (instType.equals("RET"))
    {
        pInstruction = new Instruction(InstructionType::RET, "");
    }
    else if (instType.equals("EMIT"))
    {
        pInstruction = new Instruction(InstructionType::EMIT, arg);
    }
    else
    {
        SendResponse(ResponseCode::ERROR);
        return;
    }

    Task* pTask = pProgram->GetLastCreatedTask();
    Routine* pRoutine = pTask->GetLastCreatedRoutine();
    Rung* pRung = pRoutine->GetLastCreatedRung();

    pRung->AddInstruction(pInstruction);
    SendResponse(ResponseCode::SUCCESS);
}

/**
 * @brief Finishes a download by starting each periodic task
 *
 * @param pProgram      Program that has been downloaded
*/
static void HandleEndDownload(UserProgram* pProgram)
{
    // Add all tasks to the schedule
    const List<Task*>& rTasks = pProgram->GetTaskList();
    for (int i = 0; i < rTasks.GetLength(); i++)
    {
        // Only add periodic tasks
        if (rTasks[i]->GetTaskType() == TaskType::PERIODIC)
        {
            Scheduler::GetInstance().AddTask(rTasks[i]);
        }
        else
        {
            Scheduler::GetInstance().AddEventDrivenTask(rTasks[i]);
        }
    }

    LcdApi::Clear();
    LcdApi::Write(pProgram->GetProgramName().c_str());

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
    LOGN(rData);
    // Parse the message between tag name and value
    String tagName = rData.substring(0, rData.indexOf(" "));
    bool value = atoi(rData.substring(rData.indexOf(" "), rData.length()).c_str());
    digitalWrite(LED_BUILTIN, value ? HIGH : LOW);

    // Set the tags value and send the response
    bool ret = TagDatabase::SetTag(tagName, value);
    SendResponse(static_cast<ResponseCode>(!ret));
}

/**
 * @brief Gets the values of all tags in the controller
*/
static void GetAllTagValues()
{
    String allTags = TagDatabase::GetAllTagValues();

    SendResponse(ResponseCode::SUCCESS, allTags.c_str());
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
        case RequestCode::HWTRACK_CREATE_TAG:
            HandleCreateTag(data);
            break;
        case RequestCode::HWTRACK_CREATE_TASK:
            HandleCreateTask(pUserProgram, data);
            break;
        case RequestCode::HWTRACK_CREATE_ROUTINE:
            HandleCreateRoutine(pUserProgram, data);
            break;
        case RequestCode::HWTRACK_CREATE_RUNG:
            HandleCreateRung(pUserProgram);
            break;
        case RequestCode::HWTRACK_CREATE_INSTRUCTION:
            HandleCreateInstruction(pUserProgram, data);
            break;
        case RequestCode::HWTRACK_END_DOWNLOAD:
            HandleEndDownload(pUserProgram);
            break;
        case RequestCode::HWTRACK_GET_TAG_VALUE:
            GetTagValue(data);
            break;
        case RequestCode::HWTRACK_SET_TAG_VALUE:
            SetTagValue(data);
            break;
        case RequestCode::HWTRACK_GET_ALL_TAG_VALUES:
            GetAllTagValues();
            break;
        default:
            // We expect ParseCode to take care of this case
            assert(false);
    }
}

} // namespace Communications
