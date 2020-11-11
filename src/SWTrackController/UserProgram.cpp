#include <UserProgram.hpp>

void UserProgram::ClearMemory()
{
    m_tasks.clear();
    m_pName = "";

}

void UserProgram::AddTask(Task* pTask)
{
    m_tasks.push_back(pTask);
}

Task* UserProgram::getMostRecentTask() const
{
    return m_tasks[m_tasks.size()-1];
}