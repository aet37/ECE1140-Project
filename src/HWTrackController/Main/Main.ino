/**
 * @file Main.ino
*/

// SYSTEM INCLUDES
#include <stdint.h> // For standard types

// C++ PROJECT INCLUDES
#include "include/Communications.hpp" // For Communications::CommsTask
#include "include/Scheduler.hpp" // For Scheduler
#include "include/UserProgram.hpp" // For UserProgram
#include "include/Lcd/LcdApi.hpp" // For LcdApi
#include "include/TagDatabase.hpp" // For TagDatabase
#include "include/SystemTask.hpp" // For SystemTask
#include "include/ArduinoLogger.hpp" // For LOG

static uint64_t currentTime;

void setup()
{
    // Initialize Serial
    Serial.begin(9600);

    // Initialize the lcd display
    LcdApi::Initialize();

    // Pin Initialization
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(PIN2, OUTPUT);
    pinMode(PIN3, OUTPUT);

    // Initialize the user program
    UserProgram* pProg = new UserProgram("Blank Program");
    LcdApi::Write("Blank Program");

    // Add tasks to the scheduler
    Scheduler::GetInstance().AddTask(new SystemTask(toggleTask, nullptr, 1000));
    Scheduler::GetInstance().AddTask(new SystemTask(LcdApi::ScrollTask, nullptr, 500));
    Scheduler::GetInstance().AddTask(new SystemTask(Communications::CommsTask, static_cast<void*>(pProg), 100));
    Scheduler::GetInstance().AddTask(new SystemTask(TagDatabase::IoTask, nullptr, 100));
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
