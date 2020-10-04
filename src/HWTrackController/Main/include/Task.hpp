/**
 * @file Task.hpp
*/
#ifndef TASK_HPP
#define TASK_HPP

// SYSTEM INCLUDES
#include <stdint.h>

// C++ PROJECT INCLUDES
// (None)

/**
 * @class Task
 * 
 * @brief Data structure to represent a
 * periodic task
*/
class Task
{
public:
    /// Typedef for task function
    typedef void (*TaskFunction)(void*);

    /**
     * @brief Creates a new Task object
    */
    Task(TaskFunction func, uint32_t periodInMs) :
        m_periodInMs(periodInMs),
        m_timeLastRunInMs(0),
        m_taskFunction(func)
    {}

    /// Delete assignment constructor
    Task& operator=(Task const&) = delete;

    /// Delete copy constructor
    Task(Task const&) = delete;

    /**
     * 
    */
    Task operator()()
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
    TaskFunction m_taskFunction;
};

#endif // TASK_HPP
