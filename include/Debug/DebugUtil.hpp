/////////////////////////////////
/// @file DebugUtil.hpp
///
/// @brief Utility functions and macros
/// used by debug functions/classes
/////////////////////////////////
#ifndef DEBUG_UTIL_HPP
#define DEBUG_UTIL_HPP

// SYSTEM INCLUDES
#include <cstdarg>
#include <string>
#include <cstring>

// C++ PROJECT INCLUDES
// (None)

// FORWARD DECLARATIONS
// (None)

// MACROS
// Strip the path off of __FILE__
#define __FILENAME__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)

// Accept any number of args >= N, but expand to just the Nth one. In this case,
// we have settled on 9 as N. We could pick a different number by adjusting
// the count of throwaway args before N. Note that this macro is preceded by
// an underscore--it's an implementation detail, not something we expect people
// to call directly.
#define _GET_NTH_ARG(_1, _2, _3, _4, _5, _6, _7, _8, _9, N, ...) N

// Count how many args are in a variadic macro. Only works for up to N-1 args.
#define _COUNT_VARARGS(...) _GET_NTH_ARG("ignored", ##__VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)


////////////////////////////////
/// @brief Formats a string in the same
/// way done by printf
///
/// @param numArgs  Number of arguments including base string
/// @param valist   Initialized argument list
/// @return         A string with formats replaced
////////////////////////////////
std::string format(const int numArgs, va_list valist);

#endif
