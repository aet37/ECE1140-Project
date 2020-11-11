#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include "../../include/Devices/Devices.hpp"

namespace Devices
{
    //LCD
    static LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4);

    // Joystick
    const int SW = 52;
    const int VRx = A0;
    const int VRy = A1;
    int xPosition = 0;
    int yPosition = 0;
    int SW_state = 0;
    int mapX = 0;
    int mapY = 0;

    //Button
    const int buttonPin = 40;
    int buttonState;
    int lastButtonState = 0;
    unsigned long lastDebounceTime = 0;
    unsigned long debounceDelay = 50;

    // LCD
    void InitializeLCD()
    {
        lcd.init();
        lcd.backlight();
    }

    void WriteLCD(String& rText)
    {
        lcd.setCursor(0,0);
        lcd.print(rText);
    }

    void WriteCharLCD(char* pChar)
    {
        lcd.setCursor(0,0);
        lcd.print(pChar);
    }

    void ClearLCD()
    {
        lcd.clear();
    }

    void ScrollRight()
    {
        // MAKE SCHEDULER TO INPUT DELAY SO LCD WORKS
        lcd.scrollDisplayRight();
    }

    void ScrollTask(void* pNothing)
    {
        ScrollRight();
    }

    void InitializeJoystick()
    {
        pinMode(VRx, INPUT);
        pinMode(VRy, INPUT);
        pinMode(SW, INPUT_PULLUP);
    }

    void JoystickRead()
    {
        xPosition = analogRead(VRx);
        yPosition = analogRead(VRy);
        SW_state = digitalRead(SW);
        //if(xPosition = )
    }

    void InitializeButton()
    {
        pinMode(buttonPin, INPUT);
    }

    void ButtonClick()
    {
        buttonState = digitalRead(buttonPin);
        if(buttonState == HIGH)
        {
            
        } else {
            JoystickRead();
        }
    }
}