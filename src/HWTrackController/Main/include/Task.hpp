/**
 * @file Task.hpp
 *
 * @brief Declarations of the Task class
*/
#ifndef TASK_HPP
#define TASK_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "List.hpp" // For List
#include "SystemTask.hpp" // For SystemTask

// FORWARD REFERENCES
class Routine;

/**
 * @enum TaskType
*/
enum class TaskType
{
    PERIODIC,
    EVENT_DRIVEN
};

/**
 * @class Task
 *
 * @brief Class to represent the top level of the user's logic
*/
class Task : public SystemTask
{
public:
    /**
     * @brief Constructs a new Task object
    */
    Task(const char* pTaskName, TaskType taskType, uint32_t periodInMs = 0) :
        SystemTask(Run, this, periodInMs),
        m_pTaskName(pTaskName),
        m_type(taskType),
        m_routineList(),
        m_pLastCreatedRoutine(nullptr)
    {}

    /**
     * @brief Method used by the scheduler to invoke this task
     *
     * @param pTask     Pointer to the task to execute
    */
    static void Run(void* pTask);

    /**
     * @brief Runs the task starting with the main routine
    */
    void Run();

    /**
     * @brief Adds a routine to the routine list
     *
     * @param pRoutine      Routine to be added
     * @param mainRoutine   Whether this is the main routine being added
    */
    void AddRoutine(Routine* pRoutine, bool mainRoutine = false);

    /**
     * @brief Gets the last created routine
    */
    Routine* GetLastCreatedRoutine() const { return m_pLastCreatedRoutine; }

protected:
private:
    /// Type of the task
    TaskType m_type;

    /// Name of the task
    const char* m_pTaskName;

    /// List of routines belonging to this task. The first routine is the main routine
    List<Routine*> m_routineList;

    /// Last created routine
    Routine* m_pLastCreatedRoutine;
};

#endif // TASK_HPP
