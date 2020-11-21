#include <Wire.h>
#include "include/Joystick/Joystick.hpp"

namespace JoystickController
{
    const int SW = 52;
    const int VRx = A0;
    const int VRy = A1;
    int xPosition = 0;
    int yPosition = 0;
    int SW_state = 0;
    int mapX = 0;
    int mapY = 0;

    void Initialize()
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
    }


}