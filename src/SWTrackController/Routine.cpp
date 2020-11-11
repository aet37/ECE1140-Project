#include <Routine.hpp>
#include <Rung.hpp>
#include <Logger.hpp>

void Routine::Run()
{
    LOG_SW_TRACK_CONTROLLER("Running routine "); 

    for (uint32_t i = 0; i < m_rungList.getLength(); i++)
    {
        LOG_SW_TRACK_CONTROLLER("Executing rung "); 
        m_rungList[i]->Execute();
    }
}