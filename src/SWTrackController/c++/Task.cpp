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
        m_routineList.insert(m_routineList.begin(),pRoutine);
    }
    else
    {
        m_routineList.push_back(pRoutine);
    }
    m_pMostRecentMadeRoutine = pRoutine;
    
}