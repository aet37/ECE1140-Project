/**
 * @file Rung.cpp
 * 
 * @brief Implementations of Rung class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "../include/Rung.hpp" // Header for class
#include "../include/ArduinoLogger.hpp" // For LOG
#include "../include/Instruction.hpp" // For Instruction

void Rung::AddInstruction(Instruction* pInst)
{
    // TODO: Insert instruction in correct place
    m_instructions.Append(pInst);
}

void Rung::Execute()
{
    LOGN("Executing rung");

    // Execute the instructions on this rung. If an instruction evaluates to false,
    // We should stop executing this rung
    for (int i = 0; i < m_instructions.GetLength(); i++)
    {
        bool ret = m_instructions[i]->Evaluate();
        if (ret == false)
        {
            break;
        }
    }
}
