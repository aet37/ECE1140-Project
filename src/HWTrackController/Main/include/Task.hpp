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
// (None)

// FORWARD REFERENCES
class Routine;

/**
 * @class Task
 * 
 * @brief Class to represent the top level of the user's logic
*/
class Task
{
public:
    /**
     * @enum TaskType
    */
    enum class TaskType
    {
        CONTINUOUS,
        PERIODIC,
        EVENT_DRIVEN
    }

    /**
     * @brief Constructs a new Task object
    */
    Task() :
        m_type(TaskType::PERIODIC),
        m_period(0)
    {}
protected:
private:
    /// Type of the task
    TaskType m_type;

    /// Period of the task. 0 if continuous or event driven
    uint32_t m_period; 
};

#endif // TASK_HPP
