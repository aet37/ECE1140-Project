//
// Created by Nathan Swanson on 10.6.20
//

#ifndef USER_PROGRAM_HPP
#define USER_PROGRAM_HPP
#include <vector>
#include <Task.hpp>

// class that holds information on a track controller
class UserProgram
{
	private:
	std::vector<Task*> m_tasks;
    string m_pName;


	public:
	
	UserProgram(const char* name) :
        m_tasks(),
        m_pName(name)
    {}

    ~UserProgram(){}

    UserProgram() {};

    void ClearMemory();

    void setProgramName(const char* pProgramName)
    {
        m_pName = pProgramName;
    }

    const string& getProgramName() const
    {
        return m_pName;
    }

    void AddTask(Task* pTask);

    Task* getMostRecentTask() const;

    const std::vector<Task*>& getTaskList() const
    {
        return m_tasks;
    }
    


	
};





#endif 
