#include <UserProgram.hpp>

void UserProgram::ClearMemory()
{
    m_tasks.Clear();
    m_pName = "";

}

void UserProgram::AddTask(Task* pTask)
{
    m_tasks.Append(pTask);
}

Task* UserProgram::getMostRecentTask() const
{
    return m_tasks[m_tasks.getLength()-1];
}