/**
 * @file InstructionIface.hpp
 * 
 * @brief Declarations for the InstructionIface class
*/
#ifndef INSTRUCTION_IFACE_HPP
#define INSTRUCTION_IFACE_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

/**
 * @class InstructionIface
 * 
 * @brief Representation of a ladder logic instruction
*/
class InstructionIface
{
public:
    /**
     * @brief Executes the instructions on this rung
    */
    void Execute();
protected:
private:
};

#endif // INSTRUCTION_IFACE_HPP
