/**
 * @file Routine.hpp
 *
 * @brief Declarations of the Routine class
*/
#ifndef ROUTINE_HPP
#define ROUTINE_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "List.hpp" // For List
#include "Rung.hpp" // For Rung

/**
 * @class Routine
 *
 * @brief Class to represent routines that may run
 * within the user's tasks
*/
class Routine
{
public:
    /**
     * @brief Constructs a new Routine object
    */
    Routine() :
        m_pRoutineName(),
        m_pFirstRung(nullptr)
    {}

    /**
     * @brief Runs this routine beginning with the first rung
    */
    void Run();
protected:
private:
    /// Name of the routine
    const char* m_pRoutineName;

    /// Pointer to the first rung in the routine
    Rung* m_pFirstRung;
};

#endif // ROUTINE_HPP
