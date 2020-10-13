/**
 * @file CTCMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "CTCMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros

namespace CTC
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_CTC("Thread starting...");
}

} // namespace CTC
