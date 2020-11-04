/**
 * @file UserProgram.cpp
 * 
 * @brief Implementations of UserProgram class
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/UserProgram.hpp" // Header for class

void UserProgram::ClearMemory()
{
    m_tasks.Clear();
    m_pProgramName = "";
}

void UserProgram::AddTask(Task* pTask)
{
    m_tasks.Append(pTask);
}

Task* UserProgram::GetLastCreatedTask() const
{
    return m_tasks[m_tasks.GetLength() - 1];
}
