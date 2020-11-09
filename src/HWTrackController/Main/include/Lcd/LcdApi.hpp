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

/**
 * @brief Writes the given text to the display starting at (0, 0)
*/
void Write(String& rText);
void Write(const char* pText);

/**
 * @brief Clears the LCD display
*/
void Clear();

/**
 * @brief Scrolls the text to the right
*/
void ScrollRight();

/**
 * @brief Task function to periodically scroll the display
*/
void ScrollTask(void* pNothing);

} // namespace LcdApi

#endif // LCD_API_HPP
