/**
 * @file Main.ino
*/

// SYSTEM INCLUDES
#include <stdint.h> // For standard types

// C++ PROJECT INCLUDES
#include "include/Communications.hpp" // For Communications::CommsTask
#include "include/Scheduler.hpp" // For Scheduler

static uint64_t currentTime;

void setup()
{
    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);

    Scheduler::GetInstance().AddTask(new Task(toggleTask, 1000));
    Scheduler::GetInstance().AddTask(new Task(Communications::CommsTask, 1000));
}

void loop()
{
    Scheduler::GetInstance().RunTasks();
}

void toggleTask(void* something)
{
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.write("LED Toggled\n");
}
