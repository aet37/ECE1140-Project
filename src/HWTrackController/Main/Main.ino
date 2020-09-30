/**
 * @file Main.ino
*/

// SYSTEM INCLUDES
#include <stdint.h> // For standard types

// C++ PROJECT INCLUDES
// (None)

static uint64_t currentTime;

void setup()
{
    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    // Get the current time
    currentTime = millis();

    toggleTask();
}

void toggleTask()
{
    const uint32_t period = 1000;
    static uint64_t lastUpdateTime = 0;

    if (currentTime - lastUpdateTime >= period)
    {
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
        lastUpdateTime = currentTime;
    }
}
