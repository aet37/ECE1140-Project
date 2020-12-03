#include "include/HWTrainCommunications.hpp"
#include "include/Devices/Devices.hpp"
#include "include/Scheduler.hpp"


void setup()
{
  Serial.begin(9600);

  Devices::InitializeLCD();
  Devices::InitializeJoystick();
  Devices::InitializeButton();

 
  // Initialize the LCD
  Devices::WriteCharLCD("WELCOME");
}

void loop()
{
  HWTrainCommunications::CommsTask();
}
