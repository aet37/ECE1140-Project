#include <Wire.h>
#include "../../include/Button/Button.hpp"

namespace Button
{

    const int buttonPin = 40;
    int buttonState;
    int lastButtonState = 0;
    unsigned long lastDebounceTime = 0;
    unsigned long debounceDelay = 50;

    void Initialize()
    {
        pinMode(buttonPin, INPUT);
    }

    void ButtonClick()
    {
        buttonState = digitalRead(buttonPin);
        if(buttonState == HIGH)
        {
            
        } else {
            
        }
    }

}