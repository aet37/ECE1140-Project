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

void WriteTest()
{
    lcd.setCursor(0, 0); // Set the cursor on the first column and first row.
    lcd.print("Hello World!"); // Print the string "Hello World!"
    lcd.setCursor(2, 1); //Set the cursor on the third column and the second row (counting starts at 0!).
    lcd.print("LCD tutorial");
}

void ScrollRight()
{
    lcd.scrollDisplayRight();
}

} // namespace LcdApi
