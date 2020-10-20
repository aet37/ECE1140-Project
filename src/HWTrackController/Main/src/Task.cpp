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
    LOG("Running task "); LOGN(m_pTaskName);

    // Execute the main routine
    m_routineList[0]->Run();
}

void Task::AddRoutine(Routine* pRoutine)
{
    m_routineList.Append(pRoutine);
}
