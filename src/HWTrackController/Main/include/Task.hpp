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
#include "Routine.hpp" // For Routine

/**
 * @enum TaskType
*/
enum class TaskType
{
    CONTINUOUS,
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
    Task(TaskType taskType, uint32_t periodInMs = 0) :
        SystemTask(Run, this, periodInMs),
        m_type(taskType)
    {}

    /**
     * @brief Method used by the scheduler to invoke this task
     * 
     * @param pTask     Pointer to the task to execute
    */
    static void Run(void* pTask);

    /**
     * @brief 
    */
    void Run();
protected:
private:
    /// Type of the task
    TaskType m_type;

    /// Name of the task
    const char* m_pTaskName;

    /// List of routines belonging to this task. The first routine is the main routine
    List<Routine> m_routineList;
};

#endif // TASK_HPP
