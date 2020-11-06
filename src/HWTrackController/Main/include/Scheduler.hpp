/**
 * @file Scheduler.hpp
 *
 * @brief Declaration of the Scheduler class
*/
#ifndef SCHEDULER_HPP
#define SCHEDULER_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "List.hpp" // For List

// FORWARD REFERENCES
class UserProgram;
class SystemTask;
class Task;

/**
 * @class Scheduler
 *
 * @brief Class responsible for scheduling
 * and running tasks
*/
class Scheduler
{
public:
    /**
     * @brief Gets the singleton instance
    */
    static Scheduler& GetInstance()
    {
        static Scheduler* pInstance = new Scheduler();
        return *(pInstance);
    }

    /**
     * @brief Adds a task to the schedule
     *
     * @param pTask     Task to be added
    */
    void AddTask(SystemTask* pTask)
    {
        m_taskList.Append(pTask);
    }

    /**
     * @brief Adds a task to the event driven task list
     *
     * @param pTask     Task to be added
    */
    void AddEventDrivenTask(Task* pTask)
    {
        m_eventDrivenTaskList.Append(pTask);
    }

    /**
     * @brief Runs through tasks and executes
     * those that need run
    */
    void RunTasks();

    /**
     * @brief Runs an event driven task with the given event name
     *
     * @param rEventName        Name of the event that was triggered
     * @return Whether any task was run
    */
    bool RunEventDrivenTask(const String& rEventName);

    /**
     * @brief Removes all user tasks from the schedule
    */
    void RemoveUserTasks();

protected:
private:
    /// List of tasks
    List<SystemTask*> m_taskList;

    /// List of event driven tasks
    List<Task*> m_eventDrivenTaskList;

    /**
     * @brief Creates a new Scheduler object
    */
    Scheduler() :
        m_taskList(),
        m_eventDrivenTaskList(5)
    {}
};

#endif // SCHEDULER_HPP
