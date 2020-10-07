/////////////////////////////////
/// @file Logger.cpp
///
/// @brief Implementations for Logger class
/////////////////////////////////

// SYSTEM INCLUDES
#include <iostream>
#include <string>
#include <sstream>

// C PROJECT INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // Header for class

////////////////////////////////
/// METHOD NAME: Logger::Log
////////////////////////////////
void Logger::Log(const std::string& rMsg, const Logger::LogLevel logLevel, const Logger::PrintGroup printGroup)
{
    // Print log level
    m_logStream << LOG_LEVEL_NAMES[static_cast<uint8_t>(logLevel)] << " : ";

    // Print print group
    m_logStream << PRINT_GROUP_NAMES[static_cast<uint8_t>(printGroup)] << " : ";

    // Print message
    m_logStream << rMsg << "\n";

    // Flush the log
    m_logStream.flush();
}

////////////////////////////////
/// METHOD NAME: Logger::Log
////////////////////////////////
void Logger::Log(const char* fileName, const char* funcName, const int lineNumber, const Logger::LogLevel logLevel, const Logger::PrintGroup printGroup, const int numArgs, ...)
{
    // Concatenate given strings
    std::stringstream concatStream;
    concatStream << fileName << " : " << funcName << " : Line " << lineNumber << " : ";

    // Initialize valist
    va_list valist;
    va_start(valist, numArgs);

    // Concatenate given strings
    std::string message = format(numArgs, valist);
    concatStream << message;

    // Clean up memory
    va_end(valist);

    // Have to copy it because of how .str() works
    std::string concatString = concatStream.str();
    Log(concatString, logLevel, printGroup);

    // Add your module's printgroup here for them to also be printed to the console
    if (printGroup == Logger::PrintGroup::PRINT_GROUP_SERVER)
    {
        std::cout << message << std::endl;
    }
}