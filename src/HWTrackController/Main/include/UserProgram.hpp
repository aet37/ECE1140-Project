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
#include "../include/HashMap.hpp" // For HashMap

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
     * Constructs a new UserProgram object
     */
    UserProgram() :
        m_keys(),
        m_pProgramName("Test Program")
    {}
    
protected:
private:
    /// Tags of the program
    HashMap<bool> m_keys;

    /// Name of the program
    const char* m_pProgramName;
};

#endif // USER_PROGRAM_HPP