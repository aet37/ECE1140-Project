/**
 * @file UserProgram.hpp
 *
 * @brief Declarations of the UserProgram class
*/
#ifndef USER_PROGRAM_HPP
#define USER_PROGRAM_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "List.hpp" // For List

// FORWARD REFERENCES
class Task;

/**
 * @class UserProgram
 *
 * @brief Class to represent the user program.
 * This class gets built when the user downloads a program
*/
class UserProgram
{
public:
    /**
     * @brief Constructs a new UserProgram object
     */
    explicit UserProgram(const char* pProgramName) :
        m_tasks(),
        m_pProgramName(pProgramName)
    {}

    /**
     * @brief Destroys the UserProgram object
    */
    ~UserProgram() {}

    /**
     * @brief Clears all tasks, routines, rungs, and instructions from the program
    */
    void ClearMemory();

    /**
     * @brief Sets the program name
    */
    void SetProgramName(const char* pProgramName) { m_pProgramName = pProgramName; }

    /**
     * @brief Adds the given task to the task list
    */
    void AddTask(Task* pTask);

    /**
     * @brief Gets the last task in the list
    */
    Task* GetLastCreatedTask() const;

protected:
private:
    /// List of tasks included within the program
    List<Task*> m_tasks;

    /// Name of the program
    const char* m_pProgramName;
};

#endif // USER_PROGRAM_HPP
