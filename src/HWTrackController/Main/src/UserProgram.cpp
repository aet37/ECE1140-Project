/**
 * @file UserProgram.cpp
 * 
 * @brief Implementations of UserProgram class
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/UserProgram.hpp" // Header for class

void UserProgram::AddTag(const char* pTagName)
{
    m_tags.Insert(pTagName, false);
}

bool UserProgram::SetTag(String& rTagName, bool value)
{
    return m_tags.Update(rTagName, value);
}

bool UserProgram::GetTagValue(String& rTagName, bool& rValue)
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
