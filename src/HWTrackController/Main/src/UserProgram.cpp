/**
 * @file UserProgram.cpp
 * 
 * @brief Implementations of UserProgram class
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/UserProgram.hpp" // Header for class

void UserProgram::AddTask(Task* pTask)
{
    m_tasks.Append(pTask);
}
