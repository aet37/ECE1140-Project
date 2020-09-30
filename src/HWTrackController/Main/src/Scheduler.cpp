/**
 * @file Scheduler.cpp
 * 
 * @brief Implementations of the Scheduler class
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "Scheduler.hpp" // Header for class

/// Current system time
static uint64_t currentTimeInMs;

void Scheduler::RunTasks()
{
    currentTimeInMs = millis();

    // For every task...
    for (int i = 0; i < m_taskList.GetLength(); i++)
    {
        Task* pTask = m_taskList[i];

        // If it's 
        if (currentTimeInMs - pTask->GetTimeLastRun() >= pTask->GetPeriod())
        {
            pTask->operator()();
            pTask->SetTimeLastRun(currentTimeInMs);
        }
    }
}