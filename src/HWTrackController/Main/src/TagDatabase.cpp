/**
 * @file TagDatabase.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDE
#include "../include/TagDatabase.hpp" // Header for functions
#include "../include/HashMap.hpp" // For HashMap

#define PIN23 23

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

void Clear()
{
    tags.Clear();
}

static void ReadInputs()
{
    static bool flipped = false;
    if (!digitalRead(PIN23) && !flipped)
    {
        SetTag("switch", !digitalRead(PIN3));
        flipped = true;
    }
    else if (digitalRead(PIN23))
    {
        flipped = false;
    }
}

void IoTask(void* pSomething)
{
    // Read the input pins
    ReadInputs();

    bool tagValue = false;
    if (GetTagValue("output2", tagValue))
    {
        digitalWrite(PIN2, tagValue);
    }

    if (GetTagValue("switch", tagValue))
    {
        digitalWrite(PIN3, tagValue);
    }
}

} // namespace TagDatabase
