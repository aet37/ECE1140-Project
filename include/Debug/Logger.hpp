/////////////////////////////////
/// @file Logger.hpp
///
/// @brief Declaration of Logger class
/////////////////////////////////
#ifndef LOGGER_HPP
#define LOGGER_HPP

// SYSTEM INCLUDES
#include <string.h>
#include <fstream>
#include <string>

// C++ PROJECT INCLUDES
#include "DebugUtil.hpp" // For util macros

// FORWARD DECLARATIONS
// (None)

// Internal Macros
#define LOG_INTERNAL(logLevel, printGroup, ...) Logger::GetInstance().Log(__FILENAME__, __PRETTY_FUNCTION__, \
                                                __LINE__, logLevel, printGroup, _COUNT_VARARGS(__VA_ARGS__), ##__VA_ARGS__)
#define LOG_DEBUG_INTERNAL(printGroup , ...) LOG_INTERNAL(Logger::LogLevel::DEBUG, printGroup, ##__VA_ARGS__)

// Public Macros
// General prints
#define LOG_DEBUG(...) LOG_INTERNAL(Logger::LogLevel::DEBUG, Logger::PrintGroup::PRINT_GROUP_GENERAL, ##__VA_ARGS__)
#define LOG_INFO(...) LOG_INTERNAL(Logger::LogLevel::INFO, Logger::PrintGroup::PRINT_GROUP_GENERAL, ##__VA_ARGS__)
#define LOG_ERROR(...) LOG_INTERNAL(Logger::LogLevel::ERROR, Logger::PrintGroup::PRINT_GROUP_GENERAL, ##__VA_ARGS__)

// Print groups
#define LOG_GENERAL(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_GENERAL, ##__VA_ARGS__)
#define LOG_SERVER(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_SERVER, ##__VA_ARGS__)
#define LOG_CTC(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_CTC, ##__VA_ARGS__)
#define LOG_SW_TRACK_CONTROLLER(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_SW_TRACK_CONTROLLER, ##__VA_ARGS__)
#define LOG_HW_TRACK_CONTROLLER(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_HW_TRACK_CONTROLLER, ##__VA_ARGS__)
#define LOG_TRACK_MODEL(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_TRACK_MODEL, ##__VA_ARGS__)
#define LOG_TRAIN_MODEL(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_TRAIN_MODEL, ##__VA_ARGS__)
#define LOG_SW_TRAIN_CONTROLLER(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_SW_TRAIN_CONTROLLER, ##__VA_ARGS__)
#define LOG_HW_TRAIN_CONTROLLER(...) LOG_DEBUG_INTERNAL(Logger::PrintGroup::PRINT_GROUP_HW_TRAIN_CONTROLLER, ##__VA_ARGS__)

////////////////////////////////
/// @class Logger
///
/// @brief The logger class is used to
/// print debug messages while the program
/// is executing
////////////////////////////////
class Logger
{
public:
    /////////////////////////////////////
    /// @brief Gets the singleton instance
    ///
    /// @return Logger instance
    /////////////////////////////////////
    static Logger& GetInstance()
    {
        /// Singleton instance
        static Logger* instance = new Logger();
        return *instance;
    }

    ////////////////////////////////
    /// @enum LogLevel
    ///
    /// @note The values of these enums are
    /// used to index the LOG_LEVEL_NAMES array
    ////////////////////////////////
    enum class LogLevel : uint8_t
    {
        INFO = 0,
        DEBUG = 1,
        ERROR = 2
    };

    ////////////////////////////////
    /// @enum PrintGroup
    ///
    /// @note The values of these enums are
    /// used to index the PRINT_GROUP_NAMES array
    ////////////////////////////////
    enum class PrintGroup : uint8_t
    {
        PRINT_GROUP_GENERAL = 0,
        PRINT_GROUP_SERVER = 1,
        PRINT_GROUP_CTC = 2,
        PRINT_GROUP_SW_TRACK_CONTROLLER = 3,
        PRINT_GROUP_HW_TRACK_CONTROLLER = 4,
        PRINT_GROUP_TRACK_MODEL = 5,
        PRINT_GROUP_TRAIN_MODEL = 6,
        PRINT_GROUP_SW_TRAIN_CONTROLLER = 7,
        PRINT_GROUP_HW_TRAIN_CONTROLLER = 8,
        PRINT_GROUP_ASSERT = 9
    };

    ////////////////////////////////
    /// @brief This version is used for the
    /// log macro. It's called after finding
    /// the number of arguments
    ///
    /// @warning This method is only to be used through the macro
    /// defined above.
    ///
    /// @param fileName     Name of file where assert is placed
    /// @param funcName     Name of the function where the assert is placed
    /// @param lineNumber   Line on which assert is placed
    /// @param logLevel     Level at which to print message
    /// @param printGroup   Name of group to which print belongs
    /// @param numArgs      Number of arguments passed in additionally
    /// @param ...          Format string followed by replacement variables
    ////////////////////////////////
    void Log(const char* fileName, const char* funcName, const int lineNumber, const LogLevel logLevel, const PrintGroup printGroup,
             const int numArgs, ...);

    ////////////////////////////////
    /// @brief This version is used for the
    /// assert macro. It's called after finding
    /// the number of arguments
    ///
    /// @param rMsg         Message to output
    /// @param logLevel     Level at which to print message
    /// @param printGroup   Group to which this print belongs
    ////////////////////////////////
    void Log(const std::string& rMsg, const LogLevel logLevel, const PrintGroup printGroup = PrintGroup::PRINT_GROUP_GENERAL);

    /////////////////////////////////////
    /// @brief Closes the log file
    /////////////////////////////////////
    void Close() { m_logStream.close(); }

protected:
private:
    /// File name to output
    const char* LOG_FILENAME = "Debug.log";

    /// Output file stream
    std::ofstream m_logStream;

    /// Names of log levels
    const char* LOG_LEVEL_NAMES[3] =
    {
        "INFO",
        "DEBUG",
        "ERROR"
    };

    /// Names of print groups
    const char* PRINT_GROUP_NAMES[10] =
    {
        "GENERAL",
        "SERVER",
        "CTC",
        "SW_TRACK_CONTROLLER",
        "HW_TRACK_CONTROLLER",
        "TRACK_MODEL",
        "TRAIN_MODEL",
        "SW_TRAIN_CONTROLLER",
        "HW_TRAIN_CONTROLLER",
        "ASSERT"
    };

    /////////////////////////////////////
    /// @brief Constructs a new Logger object
    ///
    /// @note Private to ensure singleton
    /////////////////////////////////////
    Logger() :
        m_logStream(std::ofstream(LOG_FILENAME, std::ofstream::out))
    {}

    ////////////////////////////////
    /// @brief Copy Constructer
    ////////////////////////////////
    Logger(Logger const&);

    ////////////////////////////////
    /// @brief Assignment operator
    ////////////////////////////////
    Logger& operator=(Logger const&);
};

#endif // LOGGER_HPP
