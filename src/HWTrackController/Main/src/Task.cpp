/**
 * @file Task.cpp
 * 
 * @brief Implementations of Task class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "../include/Task.hpp" // Header for class
#include "../include/Logger.hpp" // For LOG

void Task::Run(void* pTask)
{
    static_cast<Task*>(pTask)->Run();
}

void Task::Run()
{
    LOGN("Running task");
}
