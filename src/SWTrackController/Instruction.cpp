#include <assert.h>
#include <Tagdatabase.hpp>
#include <Instruction.hpp>

bool Instruction::Evaluate()
{
    bool result = false;
    switch(m_type)
    {
         case InstructionType::XIC:
        // Assert that the tag is found because that should be caught by the compiler
        assert(TagDatabase::getTagValue(m_argument, result));
        break;
    case InstructionType::XIO:
        assert(TagDatabase::getTagValue(m_argument, result));
        result = !result;
        break;
    case InstructionType::OTE:
    case InstructionType::OTL:
        result = TagDatabase::setTag(m_argument, true);
        assert(result);
        break;
    case InstructionType::OTU:
        result = TagDatabase::setTag(m_argument, false);
        assert(result);
        break;
    default:
        assert(false);
        break;
    }

    return result;
}
