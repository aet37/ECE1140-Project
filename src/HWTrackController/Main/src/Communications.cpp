/**
 * @file Communications.cpp
*/

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "../include/Communications.hpp" // Header for class

namespace Communications
{

void CommsTask(void* something)
{
    int receivedData = Serial.read();
    if (receivedData != -1)
    {
        Serial.write("I received ");
        Serial.println(receivedData, DEC);
    }
}

} // namespace Communications