/**
 * @file TagDatabase.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDE
#include "../include/TagDatabase.hpp" // Header for functions
#include "../include/HashMap.hpp" // For HashMap

namespace TagDatabase
{

/// Tags in the controller
static HashMap<bool> tags;

void AddTag(const char* pTagName)
{
    tags.Insert(pTagName, false);
}

bool SetTag(const String& rTagName, bool value)
{
    return tags.Update(rTagName, value);
}

bool GetTagValue(const String& rTagName, bool& rValue)
{
    if (tags.Contains(rTagName))
    {
        rValue = tags.Get(rTagName);
        return true;
    }
    else
    {
        return false;
    }
}

} // namespace TagDatabase
