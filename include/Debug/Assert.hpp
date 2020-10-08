/////////////////////////////////
/// @file Assert.hpp
///
/// @brief Declaration of Assert functions
///
/// @details These functions are used in place
/// of the traditional assert method. They allow
/// for more information to be included when
/// an assert statement is added
/////////////////////////////////
#ifndef ASSERT_HPP
#define ASSERT_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "DebugUtil.hpp"

// FORWARD DECLARATIONS
// (None)

// MACROS

/// This macro is to be used to in place of the traditional assert statement
/// in order to pass along more information in the case that the expression is
/// false.
#define ASSERT(expr, ...) Assert(expr, __FILENAME__, __LINE__, _COUNT_VARARGS(__VA_ARGS__), ##__VA_ARGS__)

////////////////////////////////
/// @brief This function wraps the traditional
/// assert statement. If false, this function
/// will print the provided messages to the debug
/// log prior to asserting. It should only be called
/// using the ASSERT macro defined above
///
/// @warning This function is not to be called. It's
/// included in the above macro
///
/// @note USAGE: ASSERT(expression, format string, ...)
///
/// @param expr         Expression to be asserted
/// @param fileName     Name of file where assert is placed
/// @param lineNumber   Line on which assert is placed
/// @param numArgs      Number of arguments passed in additionally
/// @param ...          Format string followed by replacement variables
////////////////////////////////
void Assert(bool expr, const char* fileName, const int lineNumber, const int numArgs, ...);

#endif // ASSERT_HPP
