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
#include "../include/TagDatabase.hpp" // For TagDatabase

void Rung::AddInstruction(Instruction* pInst)
{
    // TODO(ljk55): Insert instruction in correct place
    m_instructions.Append(pInst);
}

void Rung::Execute()
{
    // Execute the instructions on this rung. If an instruction evaluates to false,
    // We should stop executing this rung
    bool ret = true;
    for (int i = 0; i < m_instructions.GetLength(); i++)
    {
        if (ret == true)
        {
            LOG("Executing instruction "); LOG_DECN(i);
            ret = m_instructions[i]->Evaluate();
        }
        else
        {
            // Check for OTE instructions and set their associated tags low
            if (m_instructions[i]->GetInstructionType() == InstructionType::OTE)
            {
                (void)TagDatabase::SetTag(m_instructions[i]->GetArgument(), false);
            }
        }
    }
}
