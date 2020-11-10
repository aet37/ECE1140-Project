#ifndef ROUTINE_HPP
#define ROUTINE_HPP

#include <List.hpp>
#include <Rung.hpp>


class Routine
{
    private:

        const string m_routineName;

        List<Rung*> m_rungList;

    public:

        Routine(const char* pRoutineName) :
        m_routineName(pRoutineName),
        m_rungList()
        {}

        void Run();

        void AppendRung(Rung* pRung)
        {
            m_rungList.Append(pRung);
        }

        Rung* getMostRecentMadeRung() const
        {
            return m_rungList[m_rungList.getLength()-1];
        }
        
};

#endif