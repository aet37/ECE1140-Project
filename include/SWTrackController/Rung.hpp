#ifndef RUNG_HPP
#define RUNG_HPP

#include <List.hpp>
#include <Instruction.hpp>

class Rung
{
    private:
        List<Instruction*> m_instructions;

    public:
        Rung():
            m_instructions()
        {}

        void AddInstruction(Instruction* pInst);

        void Execute();
};

#endif