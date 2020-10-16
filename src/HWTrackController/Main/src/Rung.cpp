/**
 * @file Rung.cpp
 * 
 * @brief Implementations of Rung class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "../include/Rung.hpp" // Header for class
#include "../include/Logger.hpp" // For LOG
#include "../include/InstructionIface.hpp" // For InstructionIface

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
