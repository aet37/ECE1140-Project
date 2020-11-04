/**
 * @file Main.ino
*/

// SYSTEM INCLUDES
#include <stdint.h> // For standard types

// C++ PROJECT INCLUDES
#include "include/Communications.hpp" // For Communications::CommsTask
#include "include/Scheduler.hpp" // For Scheduler
#include "include/UserProgram.hpp" // For UserProgram
#include "include/Task.hpp" // For Task
#include "include/Routine.hpp" // For Routine
#include "include/Rung.hpp" // For Rung
#include "include/Instruction.hpp" // For Instruction
#include "include/TagDatabase.hpp" // For TagDatabase::AddTag
#include "include/ArduinoLogger.hpp" // For LOG

static uint64_t currentTime;

void setup()
{
    // Initialize Serial
    Serial.begin(9600);

    // Pin Initialization
    pinMode(LED_BUILTIN, OUTPUT);

    // Initialize the user program
    UserProgram* pProg = new UserProgram("Blank Program");

    // Add tasks to the scheduler
    // Scheduler::GetInstance().AddTask(new SystemTask(toggleTask, nullptr, 1000));
    Scheduler::GetInstance().AddTask(new SystemTask(Communications::CommsTask, static_cast<void*>(pProg), 1000));
}

void loop()
{
    Scheduler::GetInstance().RunTasks();
}

void toggleTask(void* something)
{
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    LOG("LED Toggled\n");
}
