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

    m_pFirstRung->Execute();
}
