#ifndef SYSTEM_TASK_HPP
#define SYSTEM_TASK_HPP

#include <stdint.h>

class SystemTask
{
    public:

        typedef void (*SystemTaskFunction)(void*);

        SystemTask(SystemTaskFunction func, void* pArgument, uint32_t periodInMs) :
        m_periodInMs(periodInMs),
        m_timeLastRunInMs(0),
        m_taskFunction(func),
        m_pArgument(pArgument)
        {}

        SystemTask& operator=(SystemTask const&) = delete;

        SystemTask(SystemTask const&) = delete;

        void Execute()
        {
            m_taskFunction(m_pArgument);
        }

        uint32_t getPeriod() const
        {
            return m_periodInMs;
        }

        uint64_t getTimeLastRun() const
        {
            return m_timeLastRunInMs;
        }

        void setTimeLastRun(uint64_t timeLastRunInMs)
        {
            m_timeLastRunInMs = timeLastRunInMs;
        }

        virtual bool IsUserTask() const {return false;}

    private:

    const uint32_t m_periodInMs;

    uint64_t m_timeLastRunInMs;

    SystemTaskFunction m_taskFunction;

    void* m_pArgument;

    
};

#endif