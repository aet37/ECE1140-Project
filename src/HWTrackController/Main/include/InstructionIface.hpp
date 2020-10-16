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
     * @brief Evaluates the instruction
     * 
     * @return The result of the evaluation
     *      @retval true        - Instruction evaluated to true
     *      @retval false       - Instruction evaluated to false
    */
    virtual bool Evaluate() = 0;

protected:
private:
};

#endif // INSTRUCTION_IFACE_HPP
