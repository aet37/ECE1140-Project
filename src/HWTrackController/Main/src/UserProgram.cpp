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

void UserProgram::AddTag(const char* pTagName)
{
    m_tags.Insert(pTagName, false);
}

bool UserProgram::SetTag(const String& rTagName, bool value)
{
    return m_tags.Update(rTagName, value);
}

bool UserProgram::GetTagValue(const String& rTagName, bool& rValue) const
{
    if (m_tags.Contains(rTagName))
    {
        rValue = m_tags.Get(rTagName);
        return true;
    }
    else
    {
        return false;
    }
}
