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

bool UserProgram::SetTag(String& rTagName)
{
    return m_tags.Update(rTagName, true);
}

bool UserProgram::ResetTag(String& rTagName)
{
    return m_tags.Update(rTagName, false);
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
