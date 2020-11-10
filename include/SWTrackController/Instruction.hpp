#ifndef INSTRUCTION_HPP
#define INSTRUCTION_HPP

#include <string>
using namespace std;

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

class Instruction
{
    private:

    InstructionType m_type;

    string m_argument;

    public:

        Instruction(InstructionType type, string argument) :
            m_type(type),
            m_argument(argument)
            {}


};

#endif