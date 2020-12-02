/**
 * @file TagDatabase.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDE
#include "../include/TagDatabase.hpp" // Header for functions
#include "../include/HashMap.hpp" // For HashMap
#include "../include/Lcd/LcdApi.hpp"

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

String GetAllTagValues(uint32_t division)
{
    return tags.GetAllKeysAndValues(division);
}

static void ReadInputs()
{
    static bool flipped = false;
    if (!digitalRead(PIN23) && !flipped)
    {
        SetTag("switch", !digitalRead(PIN25));
        digitalWrite(PIN25, !digitalRead(PIN25));
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
    if (GetTagValue("out25p", tagValue))
    {
        digitalWrite(PIN25, tagValue);
    }

    if (GetTagValue("out27p", tagValue))
    {
        digitalWrite(PIN27, tagValue);
    }

    if (GetTagValue("out29p", tagValue))
    {
        digitalWrite(PIN29, tagValue);
    }

    if (GetTagValue("out31p", tagValue))
    {
        digitalWrite(PIN31, tagValue);
    }

    // Switch signal
    if (GetTagValue("out2p", tagValue))
    {
        digitalWrite(PIN2, tagValue);
    }

    if (GetTagValue("out3p", tagValue))
    {
        digitalWrite(PIN3, tagValue);
    }

    if (GetTagValue("out4p", tagValue))
    {
        digitalWrite(PIN4, tagValue);
    }

    // Station #2 signal
    if (GetTagValue("out5p", tagValue))
    {
        digitalWrite(PIN5, tagValue);
    }

    if (GetTagValue("out6p", tagValue))
    {
        digitalWrite(PIN6, tagValue);
    }

    if (GetTagValue("out7p", tagValue))
    {
        digitalWrite(PIN7, tagValue);
    }

    // Station #1 signal
    if (GetTagValue("out8p", tagValue))
    {
        digitalWrite(PIN8, tagValue);
    }

    if (GetTagValue("out9p", tagValue))
    {
        digitalWrite(PIN9, tagValue);
    }

    if (GetTagValue("out10p", tagValue))
    {
        digitalWrite(PIN10, tagValue);
    }
}

} // namespace TagDatabase
