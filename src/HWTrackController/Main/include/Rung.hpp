/**
 * @file Rung.hpp
 * 
 * @brief Declarations for the Rung class
*/
#ifndef RUNG_HPP
#define RUNG_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "List.hpp" // For List

// FORWARD DECLARATIONS
class Instruction;

/**
 * @class Rung
 * 
 * @brief Representation of a ladder logic rung
*/
class Rung
{
public:
    /**
     * @brief Constructs a new rung object
    */
    Rung() :
        m_instructions()
    {}

    /**
     * @brief Adds an instruction to the list
    */
    void AddInstruction(Instruction* pInst);

    /**
     * @brief Executes the instructions on this rung
    */
    void Execute();
protected:
private:
    /// Pointer to the next rung to be executed
    List<Instruction*> m_instructions;
};

#endif // RUNG_HPP
