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
#include "HashMap.hpp" // For HashMap
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
        m_tags(),
        m_tasks(),
        m_pProgramName(pProgramName)
    {}

    /**
     * @brief Destroys the UserProgram object
    */
    ~UserProgram() {}

    /**
     * @brief Adds the given task to the task list
    */
    void AddTask(Task* pTask);

    /**
     * @brief Adds a tag and defaults the value
     *
     * @param pTagName     Name of the tag
    */
    void AddTag(const char* pTagName);

    /**
     * @brief Sets the given tag to true
     *
     * @param rTagName   Name of tag to set
     * @param value      Value to set tag to
     * @return Whether tag was able to be set or not
    */
    bool SetTag(const String& rTagName, bool value);

    /**
     * @brief Gets a tag's value
     *
     * @param[in] rTagName   Name of the tag
     * @param[out] rValue    Value of the tag
     * @return Whether operation was successful
    */
    bool GetTagValue(const String& rTagName, bool& rValue) const;

protected:
private:
    /// Tags of the program
    HashMap<bool> m_tags;

    /// List of tasks included within the program
    List<Task*> m_tasks;

    /// Name of the program
    const char* m_pProgramName;
};

#endif // USER_PROGRAM_HPP
