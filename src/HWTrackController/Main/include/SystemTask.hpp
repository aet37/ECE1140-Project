/**
 * @file SystemTask.hpp
*/
#ifndef SYSTEM_TASK_HPP
#define SYSTEM_TASK_HPP

// SYSTEM INCLUDES
#include <stdint.h>

// C++ PROJECT INCLUDES
// (None)

/**
 * @class SystemTask
 * 
 * @brief Data structure to represent a
 * periodic task
*/
class SystemTask
{
public:
    /// Typedef for SystemTask function
    typedef void (*SystemTaskFunction)(void*);

    /**
     * @brief Creates a new SystemTask object
    */
    SystemTask(SystemTaskFunction func, uint32_t periodInMs) :
        m_periodInMs(periodInMs),
        m_timeLastRunInMs(0),
        m_taskFunction(func)
    {}

    /// Delete assignment constructor
    SystemTask& operator=(SystemTask const&) = delete;

    /// Delete copy constructor
    SystemTask(SystemTask const&) = delete;

    /**
     * 
    */
    SystemTask operator()()
    {
        m_taskFunction(nullptr);
    }

    /**
     * @brief Gets the period member
    */
    uint32_t GetPeriod() const
    {
        return m_periodInMs;
    }

    /**
     * @brief Gets the time that the task was last run
    */
    uint64_t GetTimeLastRun() const
    {
        return m_timeLastRunInMs;
    }

    /**
     * @brief Sets the time that this task was last run
    */
    void SetTimeLastRun(uint64_t timeLastRunInMs)
    {
        m_timeLastRunInMs = timeLastRunInMs;
    }

protected:
private:
    /// Period of task
    const uint32_t m_periodInMs;

    /// Time that task was last run
    uint64_t m_timeLastRunInMs;

    /// Function of task
    SystemTaskFunction m_taskFunction;
};

#endif // SYSTEM_TASK_HPP
