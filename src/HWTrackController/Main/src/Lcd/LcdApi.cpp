/**
 * @file LcdApi.cpp
 * 
 * @brief Implementation of api functions
*/

// SYSTEM INCLUDES
#include <LiquidCrystal_I2C.h>

// C++ PROJECT INCLUDES
#include "../../include/Lcd/LcdApi.hpp" // Header for functions

namespace LcdApi
{

// Address: 0x27, Rows: 4, Columns: 20
static LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4);

void Initialize()
{
    lcd.init();
    lcd.backlight();
}

void Write(String& rText)
{
    lcd.setCursor(0, 0); // Set the cursor on the first column and first row.
    lcd.print(rText);
}

void Write(const char* pText)
{
    lcd.setCursor(0, 0); // Set the cursor on the first column and first row.
    lcd.print(pText);
}

void Clear()
{
    lcd.clear();
}

void ScrollRight()
{
    lcd.scrollDisplayRight();
}

void ScrollTask(void* pNothing)
{
    ScrollRight();
}

} // namespace LcdApi
