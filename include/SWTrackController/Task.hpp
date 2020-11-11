#ifndef TASK_HPP
#define TASK_HPP

#include <vector>
#include <SystemTask.hpp>
#include <Routine.hpp>

enum class TaskType
{
    PERIODIC,
    EVENT_DRIVEN

};

class Task : public SystemTask
{
    private:

    TaskType m_type;

    string m_event;

    const string m_taskName;

    std::vector<Routine*> m_routineList;

    Routine* m_pMostRecentMadeRoutine;

    Task(const char* pTaskName, TaskType taskType, uint32_t periodInMs = 0):
    SystemTask(Run, this, periodInMs),
    m_taskName(pTaskName),
    m_event(""),
    m_type(taskType),
    m_routineList(),
    m_pMostRecentMadeRoutine(nullptr)
    {}

    void Run();

    static void Run(void* pTask);

    void AddRoutine(Routine* pRoutine, bool mainRoutine = false);

    Routine* getMostRecent() const
    {
        return m_pMostRecentMadeRoutine;
    }

    bool IsUserTask() const
    {
        return true;
    }

    TaskType getTaskType() const
    {
        return m_type;
    }

    void setEventName(string eventName) 
    {
        m_event = eventName;
    }

    const string& getEventName() const
    {
        return m_event;
    }
    
};

#endif