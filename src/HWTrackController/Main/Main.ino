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
#include "include/Logger.hpp" // For LOG

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

    // Create a single periodic task
    Task* pPeriodicTask = new Task("My Periodic Task", TaskType::PERIODIC, 500);
    pProg->AddTask(pPeriodicTask);

    // Create a main routine and add it to the task
    Routine* pMainRoutine = new Routine("Main");
    pPeriodicTask->AddRoutine(pMainRoutine);

    // Add a rung to the routine
    Rung* pRung = new Rung();
    pMainRoutine->SetFirstRung(pRung);

    // Add tasks to the scheduler
    // Scheduler::GetInstance().AddTask(new SystemTask(toggleTask, nullptr, 1000));
    Scheduler::GetInstance().AddTask(new SystemTask(Communications::CommsTask, static_cast<void*>(pProg), 1000));
    Scheduler::GetInstance().AddTask(pPeriodicTask);
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
