#include <Task.hpp>
#include <Routine.hpp>
#include <Logger.hpp>


void Task::Run(void* pTask)
{
    static_cast<Task*>(pTask)->Run();
}

void Task::Run()
{
    LOG_SW_TRACK_CONTROLLER("Running task"); 

    m_routineList[0]->Run();
}

void Task::AddRoutine(Routine* pRoutine, bool mainRoutine)
{
    if(mainRoutine)
    {
        m_routineList.Insert(pRoutine,0);
    }
    else
    {
        m_routineList.Append(pRoutine);
    }
    m_pMostRecentMadeRoutine = pRoutine;
    
}