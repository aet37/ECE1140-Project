#ifndef RUNG_HPP
#define RUNG_HPP

#include <vector>
#include <Instruction.hpp>

class Rung
{
    private:
        std::vector<Instruction*> m_instructions;

    public:
        Rung():
            m_instructions()
        {}

        void AddInstruction(Instruction* pInst);

        void Execute();
};

#endif