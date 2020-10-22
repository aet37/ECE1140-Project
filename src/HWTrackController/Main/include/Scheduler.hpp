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
#include "SystemTask.hpp" // For SystemTask
#include "List.hpp" // For List

// FORWARD REFERENCES
class UserProgram;

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
     * @brief Runs through tasks and executes
     * those that need run
    */
    void RunTasks();

protected:
private:
    /// List of tasks
    List<SystemTask*> m_taskList;

    /**
     * @brief Creates a new Scheduler object
    */
    Scheduler() :
        m_taskList()
    {}
};

#endif // SCHEDULER_HPP
