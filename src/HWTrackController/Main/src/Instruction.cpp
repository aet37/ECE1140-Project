/**
 * @file Instruction.cpp
*/

// SYSTEM INCLUDES
#include <assert.h>

// C++ PROJECT INCLUDES
#include "../include/Instruction.hpp" // Header for class
#include "../include/TagDatabase.hpp" // For TagDatabase
#include "../include/Scheduler.hpp" // For Scheduler

bool Instruction::Evaluate() const
{
    bool result = false;
    switch (m_type)
    {
    case InstructionType::XIC:
        // Assert that the tag is found because that should be caught by the compiler
        assert(TagDatabase::GetTagValue(m_argument, result));
        break;
    case InstructionType::XIO:
        assert(TagDatabase::GetTagValue(m_argument, result));
        result = !result;
        break;
    case InstructionType::OTE:
    case InstructionType::OTL:
        result = TagDatabase::SetTag(m_argument, true);
        assert(result);
        break;
    case InstructionType::OTU:
        result = TagDatabase::SetTag(m_argument, false);
        assert(result);
        break;
    case InstructionType::EMIT:
        // The compiler is expected to catch an emitted event without a task
        result = Scheduler::GetInstance().RunEventDrivenTask(m_argument);
        assert(result);
        break;
    default:
        assert(false);
        break;
    }

    return result;
}
