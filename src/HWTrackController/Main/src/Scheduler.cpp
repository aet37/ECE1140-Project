/**
 * @file Scheduler.cpp
 *
 * @brief Implementations of the Scheduler class
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/ArduinoLogger.hpp" // For LOG macros
#include "../include/Scheduler.hpp" // Header for class
#include "../include/Task.hpp" // For Task

/// Current system time
static uint64_t currentTimeInMs;

void Scheduler::RunTasks()
{
    currentTimeInMs = millis();

    // For every task...
    for (int i = 0; i < m_taskList.GetLength(); i++)
    {
        // Get the next task in the list
        SystemTask* pTask = m_taskList[i];

        // Determine if it's been this task's period
        if (currentTimeInMs - pTask->GetTimeLastRun() >= pTask->GetPeriod())
        {
            pTask->Execute();
            pTask->SetTimeLastRun(currentTimeInMs);
        }
    }
}

bool Scheduler::RunEventDrivenTask(const String& rEventName)
{
    bool taskRun = false;
    for (int i = 0; i < m_eventDrivenTaskList.GetLength(); i++)
    {
        Task* pTask = m_eventDrivenTaskList[i];

        if (pTask->GetEventName().equals(rEventName))
        {
            pTask->Execute();
            taskRun = true;
        }
    }
    return taskRun;
}

void Scheduler::RemoveUserTasks()
{
    // For every task...
    for (int i = 0; i < m_taskList.GetLength(); i++)
    {
        SystemTask* pTask = m_taskList[i];

        if (pTask->IsUserTask())
        {
            m_taskList.Remove(i);
        }
    }
}
