/**
 * @file Main.ino
*/

// SYSTEM INCLUDES
#include <stdint.h> // For standard types

// C++ PROJECT INCLUDES
#include "include/Communications.hpp" // For Communications::CommsTask
#include "include/Scheduler.hpp" // For Scheduler
#include "include/UserProgram.hpp" // For UserProgram

static uint64_t currentTime;

void setup()
{
    // Initialize Serial
    Serial.begin(9600);

    // Pin Initialization
    pinMode(LED_BUILTIN, OUTPUT);

    // Initialize the user program
    UserProgram* pProg = new UserProgram("Iteration #2 Program");
    pProg->AddTag("Switch1");

    // Add tasks to the scheduler
    Scheduler::GetInstance().AddTask(new SystemTask(toggleTask, 1000));
    Scheduler::GetInstance().AddTask(new SystemTask(Communications::CommsTask, 1000));
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
