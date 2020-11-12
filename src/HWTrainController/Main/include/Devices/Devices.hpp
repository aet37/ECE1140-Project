#ifndef Devices_HPP
#define Devices_HPP

#include <Arduino.h> 

namespace Devices
{

void InitializeLCD();

void WriteLCD(String& rText);

void WriteCharLCD(char* pChar);

void ClearLCD();

void ScrollRight();

void ScrollTask(void* pNothing);

void InitializeJoystick();

double JoystickRead(double data);

bool JoystickClick();

void InitializeButton();

void ButtonClick();

}

#endif