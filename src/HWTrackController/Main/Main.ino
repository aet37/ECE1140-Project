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

#define PIN23 23
#define PIN13 13

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
    pinMode(PIN4, OUTPUT);
    pinMode(PIN5, OUTPUT);
    pinMode(PIN6, OUTPUT);
    pinMode(PIN7, OUTPUT);
    pinMode(PIN8, OUTPUT);
    pinMode(PIN9, OUTPUT);
    pinMode(PIN10, OUTPUT);
    pinMode(PIN25, OUTPUT);
    pinMode(PIN27, OUTPUT);
    pinMode(PIN29, OUTPUT);
    pinMode(PIN23, INPUT);

    // Initialize the user program
    UserProgram* pProg = new UserProgram("Blank Program");
    LcdApi::Write("Blank Program");

    // Add tasks to the scheduler
    Scheduler::GetInstance().AddTask(new SystemTask(toggleTask, nullptr, 1000));
    Scheduler::GetInstance().AddTask(new SystemTask(LcdApi::ScrollTask, nullptr, 600));
    Scheduler::GetInstance().AddTask(new SystemTask(Communications::CommsTask, static_cast<void*>(pProg), 100));
    Scheduler::GetInstance().AddTask(new SystemTask(TagDatabase::IoTask, nullptr, 130));
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
