#ifndef ROUTINE_HPP
#define ROUTINE_HPP

#include <vector>
#include <Rung.hpp>
#include <string>
using namespace std;



class Routine
{
    private:

        const string m_routineName;

        std::vector<Rung*> m_rungList;

    public:

        Routine(const char* pRoutineName) :
        m_routineName(pRoutineName),
        m_rungList()
        {}

        void Run();

        void AppendRung(Rung* pRung)
        {
            m_rungList.push_back(pRung);
        }

        Rung* getMostRecentMadeRung() const
        {
            return m_rungList[m_rungList.size()-1];
        }
        
};

#endif