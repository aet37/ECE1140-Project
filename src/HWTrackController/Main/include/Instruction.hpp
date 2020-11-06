/**
 * @file Instruction.hpp
 * 
 * @brief Declarations for the InstructionIface class
*/
#ifndef INSTRUCTION_HPP
#define INSTRUCTION_IFACE_HPP

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
// (None)

/**
 * @enum InstructionType
*/
enum class InstructionType
{
    XIC,
    XIO,
    OTE,
    OTL,
    OTU,
    JSR,
    RET,
    EMIT
};

/**
 * @class Instruction
 * 
 * @brief Representation of a ladder logic instruction
*/
class Instruction
{
public:
    /**
     * 
    */
    Instruction(InstructionType type, String argument) :
        m_type(type),
        m_argument(argument)
    {}

    /**
     * @brief Evaluates the instruction
     * 
     * @return The result of the evaluation
     *      @retval true        - Instruction evaluated to true
     *      @retval false       - Instruction evaluated to false
    */
    bool Evaluate();

    /**
     * @brief Gets the instruction type
    */
    const InstructionType GetInstructionType() const { return m_type; }

    /**
     * @brief Gets the argument of the instruction
    */
    const String& GetArgument() const { return m_argument; }

protected:
private:
    /// Type of the instruction
    InstructionType m_type;

    /// Argument for the instruction (either tag or routine)
    String m_argument;
};

#endif // INSTRUCTION_HPP
