/**
 * @file Routine.cpp
 * 
 * @brief Implementations of Routine class
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "../include/Routine.hpp" // Header for class
#include "../include/Logger.hpp" // For LOG
#include "../include/Rung.hpp" // For Rung

void Routine::Run()
{
    LOG("Running routine "); LOGN(m_pRoutineName);

    for (uint32_t i = 0; i < m_rungList.GetLength(); i++)
    {
        m_rungList[i]->Execute();
    }
}
