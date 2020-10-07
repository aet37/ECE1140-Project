/////////////////////////////////
/// @file Assert.cpp
///
/// @brief Implementation of Assert functions
/////////////////////////////////

// SYSTEM INCLUDES
#include <assert.h>
#include <iostream>
#include <sstream>
#include <string>

// C PROJECT INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Assert.hpp" // Header for functions
#include "Logger.hpp" // For Logger class

////////////////////////////////
/// FUNCTION NAME: Assert
////////////////////////////////
void Assert(bool expr, const char* fileName, const int lineNumber, const int numArgs, ...)
{
    if (expr) return;

    // Concatenate given strings
    std::stringstream concatStream;
    concatStream << fileName << " : Line " << lineNumber << " : ";

    // Initialize valist
    va_list valist;
    va_start(valist, numArgs);

    // Format and concatenate the remaining
    concatStream << format(numArgs, valist);

    // Clean up memory
    va_end(valist);

    // We have to copy it because of how .str() works
    std::string concatString = concatStream.str();
    Logger::GetInstance().Log(concatString, Logger::LogLevel::ERROR, Logger::PrintGroup::PRINT_GROUP_ASSERT);

    std::cout << "Assertion failed: " << concatString << '\n';
    std::cout << "See Debug.log for more details\n";

    // Close the log so it's preserved
    Logger::GetInstance().Close();

    assert(expr);
}
