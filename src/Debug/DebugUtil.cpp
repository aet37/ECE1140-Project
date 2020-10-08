/////////////////////////////////
/// @file DebugUtil.cpp
///
/// @brief Implementations for debug utility functions
/////////////////////////////////

// SYSTEM INCLUDES
#include <iostream>
#include <sstream>

// C PROJECT INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "DebugUtil.hpp" // Header for functions

////////////////////////////////
/// FUNCTION NAME: format
////////////////////////////////
std::string format(const int numArgs, va_list valist)
{
    std::stringstream formattedString;

    if (numArgs > 0)
    {
        // Print out the message filling in the given parameters
        char* msg = (va_arg(valist, char*));
        while (*msg != '\0')
        {
            if (*msg == '%')
            {
                switch (*(++msg))
                {
                    case 'd':
                    case 'i':
                    {
                        int value = va_arg(valist, int);
                        formattedString << value;
                        break;
                    }
                    case 'x':
                    {
                        int value = va_arg(valist, int);
                        formattedString << std::hex << value;
                        break;
                    }
                    case 'c':
                    {
                        // va_arg only accepts types aligned to machined boundaries
                        char value = va_arg(valist, int);
                        formattedString << value;
                        break;
                    }
                    case 'f':
                    {
                        float value = va_arg(valist, double);
                        formattedString << value;
                        break;
                    }
                    case 's':
                    {
                        char* value = va_arg(valist, char*);
                        formattedString << value;
                        break;
                    }
                    case 'p':
                    {
                        void* value = va_arg(valist, void*);
                        formattedString << value;
                        break;
                    }
                    default:
                        formattedString << "Unknown format";
                }
            }
            else
            {
                formattedString << *msg;
            }
            msg++;
        }
    }

    return formattedString.str();
}
