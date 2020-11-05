/**
 * @file LcdApi.hpp
 * 
 * @brief Declaration for functions to manipulate the display
*/
#ifndef LCD_API_HPP
#define LCD_API_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

namespace LcdApi
{

/**
 * @brief Called during setup to initialize the lcd
*/
void Initialize();

void WriteTest();

void ScrollRight();

} // namespace LcdApi

#endif // LCD_API_HPP
