#include "include/HWTrainCommunications.hpp"
#include "include/Devices/Devices.hpp"
#include "include/Scheduler.hpp"


static uint64_t currentTime;

void setup()
{
  Serial.begin(9600);

  Devices::InitializeLCD();
  Devices::InitializeJoystick();
  Devices::InitializeButton();

  // Pin Initialization


  // Initialize the LCD
  Devices::WriteCharLCD("WELCOME");
}

void loop()
{
  HWTrainCommunications::CommsTask();
  //Devices::ScrollRight();
}
