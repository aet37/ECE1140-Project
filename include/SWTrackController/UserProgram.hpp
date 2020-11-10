//
// Created by Nathan Swanson on 10.6.20
//

#ifndef USER_PROGRAM_HPP
#define USER_PROGRAM_HPP
#include <List.hpp>
#include <Task.hpp>

// class that holds information on a track controller
class UserProgram
{
	private:
	List<Task*> m_tasks;
    const char* m_pName;


	public:
	
	UserProgram(const char* name) :
    
        m_tasks(),
        m_pName(name)
        {}

    ~UserProgram(){}

    void AddTask(Task* pTask);
    


	
};





#endif 
