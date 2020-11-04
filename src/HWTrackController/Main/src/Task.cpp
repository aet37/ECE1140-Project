/**
 * @file Task.cpp
 *
 * @brief Implementations of Task class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "../include/Task.hpp" // Header for class
#include "../include/ArduinoLogger.hpp" // For LOG
#include "../include/Routine.hpp" // For Routine

void Task::Run(void* pTask)
{
    static_cast<Task*>(pTask)->Run();
}

void Task::Run()
{
    LOG("Running task "); LOGN(m_taskName);

    // Execute the main routine
    m_routineList[0]->Run();
}

void Task::AddRoutine(Routine* pRoutine, bool mainRoutine)
{
    if (mainRoutine)
    {
        m_routineList.Insert(pRoutine, 0);
    }
    else
    {
        m_routineList.Append(pRoutine);
    }
    m_pLastCreatedRoutine = pRoutine;
}
