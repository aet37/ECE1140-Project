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

// FORWARD REFERENCE
class Rung;

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
    Routine(const char* pRoutineName) :
        m_pRoutineName(pRoutineName),
        m_rungList()
    {}

    /**
     * @brief Runs this routine beginning with the first rung
    */
    void Run();

    /**
     * @brief Appends a rung to the list
    */
    void AppendRung(Rung* pRung)
    {
        m_rungList.Append(pRung);
    }

    /**
     * @brief Gets the last rung that was created
    */
    Rung* GetLastCreatedRung() const { return m_rungList[m_rungList.GetLength() - 1]; }

protected:
private:
    /// Name of the routine
    const char* m_pRoutineName;

    /// List of rungs in the routine
    List<Rung*> m_rungList;
};

#endif // ROUTINE_HPP
