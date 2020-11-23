#include <assert.h>
#include <Arduino.h>

#include "../include/HWTrainCommunications.hpp"
#include "../include/Devices/Devices.hpp"

namespace HWTrainCommunications
{
static bool lights;
static bool brake;
static bool ebrake;
static bool doors;
static bool announce;
static bool pebrake;
static bool sigfail, engfail, brakefail;
static bool ads;
static double temp, speed, kp, ki, power;
unsigned long currentTime, previousTime = 0;
const long interval = 1000;
// Determines the request code
static RequestCode ParseCode(const String& rMsg)
{
    int spaceIndex = rMsg.indexOf(' ');
    int code;
    if (spaceIndex == -1)
    {
        code = atoi(rMsg.c_str());
    }
    else
    {
        String codeString = rMsg.substring(0, spaceIndex);
        code = atoi(codeString.c_str());
    }

    switch (code)
    {
        case static_cast<int>(RequestCode::HWTRAIN_PULL_EBRAKE):
        case static_cast<int>(RequestCode::HWTRAIN_SET_SETPOINT_SPEED):
        case static_cast<int>(RequestCode::HWTRAIN_PRESS_SERVICE_BRAKE):
        case static_cast<int>(RequestCode::HWTRAIN_TOGGLE_DAMN_DOORS):
        case static_cast<int>(RequestCode::HWTRAIN_TOGGLE_CABIN_LIGHTS):
        case static_cast<int>(RequestCode::HWTRAIN_SET_TEMPERATURE):
        case static_cast<int>(RequestCode::HWTRAIN_ANNOUNCE_STATIONS):
        case static_cast<int>(RequestCode::HWTRAIN_DISPLAY_ADS):
        case static_cast<int>(RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST):
        case static_cast<int>(RequestCode::HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE):
        case static_cast<int>(RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE):
        case static_cast<int>(RequestCode::HWTRAIN_DISPATCH_TRAIN):
        case static_cast<int>(RequestCode::HWTRAIN_UPDATE_CURRENT_SPEED):
        case static_cast<int>(RequestCode::HWTRAIN_UPDATE_COMMAND_SPEED):
        case static_cast<int>(RequestCode::HWTRAIN_UPDATE_AUTHORITY):
        case static_cast<int>(RequestCode::HWTRAIN_SIGNAL_FAILURE):
        case static_cast<int>(RequestCode::HWTRAIN_PULL_PASSENGER_EBRAKE):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_GATHER_DATA):
        case static_cast<int>(RequestCode::HWTRAIN_ENGINE_FAILURE):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_SET_KP):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_GET_MODE):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_DISPLAY_POWER):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_SET_KI):
        case static_cast<int>(RequestCode::HWTRAIN_BRAKE_FAILURE):


            return static_cast<RequestCode>(code);
        default:
            return RequestCode::INVALID;
    }
}

static String ParseData(const String& rMsg)
{
    int spaceIndex = rMsg.indexOf(' ');
    if (spaceIndex == -1)
    {
        return "";
    }
    else
    {
        return rMsg.substring(spaceIndex + 1, rMsg.length());
    }
}

static void SendResponse(ResponseCode respCode, const char* pData = "")
{
    Serial.print(static_cast<int>(respCode), DEC);
    Serial.print(" ");
    Serial.println(pData);
}

static void SetLights(const String& rData)
{
    lights = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, lights ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetLights(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, lights ? "1" : "0");
    if(lights==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Lights are on");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Lights are off");
    }
}

static void SetBrake(const String& rData)
{
    brake = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, brake ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetBrake(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, brake ? "1" : "0");
    if(brake==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Brakes are on");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Brakes are off");
    }
}

static void SetAnnounce(const String& rData)
{
    announce = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, announce ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetAnnounce(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, announce ? "1" : "0");
    if(announce==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Announcements are on");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Announcements are off");
    }
}

static void SetEBrake(const String& rData)
{
    ebrake = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, ebrake ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetEBrake(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, ebrake ? "1" : "0");
    if(ebrake==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Emergency Brakes are on");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Emergency Brakes are off");
    }
}

static void SetPEBrake(const String& rData)
{
    pebrake = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, pebrake ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetPEBrake(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, pebrake ? "1" : "0");
    if(pebrake==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Passenger Emergency Brakes are on");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Passenger Emergency Brakes are off");
    }
}

static void SetSignalFailure(const String& rData)
{
    sigfail = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, sigfail ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetSignalFailure(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, sigfail ? "1" : "0");
    if(sigfail==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Signal Failure");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("No Signal Failure");
    }
}

static void SetEngineFailure(const String& rData)
{
    engfail = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, engfail ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetEngineFailure(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, engfail ? "1" : "0");
    if(engfail==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Engine Failure");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("No Engine Failure");
    }
}

static void SetBrakeFailure(const String& rData)
{
    brakefail = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, brakefail ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetBrakeFailure(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, brakefail ? "1" : "0");
    if(brakefail==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Brake Failure");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("No Brake Failure");
    }
}

static void SetDoors(const String& rData)
{
    doors = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, doors ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetDoors(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, doors ? "1" : "0");
    if(doors==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Doors are open");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Doors are closed");
    }
}

static void SetAds(const String& rData)
{
    ads = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    digitalWrite(LED_BUILTIN, ads ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetAds(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, ads ? "1" : "0");
    if(ads==1)
    {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Ads are on");
    } else {
        Devices::ClearLCD();
        Devices::WriteCharLCD("Ads are off");
    }
}

static void DisplayTemp(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggle = Devices::JoystickClick();
    temp = atof(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    while(toggle)
    {
        currentTime = millis();
        Serial.println(temp);
        temp = Devices::JoystickRead(temp);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(temp);
            Devices::WriteLCD(str);
        }
        toggle = Devices::JoystickClick();
    }
}

// 

static void DisplaySpeed(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggle = Devices::JoystickClick();
    speed = atof(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    while(toggle)
    {
        currentTime = millis();
        Serial.println(speed);
        speed = Devices::JoystickRead(speed);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(speed);
            Devices::WriteLCD(str);
        }
        toggle = Devices::JoystickClick();
    }
}

static void DisplayKi(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggle = Devices::JoystickClick();
    ki = atof(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    while(toggle)
    {
        currentTime = millis();
        Serial.println(ki);
        ki = Devices::JoystickRead(ki);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(ki);
            Devices::WriteLCD(str);
        }
        toggle = Devices::JoystickClick();
    }
}

static void DisplayKp(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggle = Devices::JoystickClick();
    kp = atof(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    while(toggle)
    {
        currentTime = millis();
        Serial.println(kp);
        kp = Devices::JoystickRead(kp);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(kp);
            Devices::WriteLCD(str);
        }
        toggle = Devices::JoystickClick();
    }
}

static void DisplayPower(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggle = Devices::JoystickClick();
    power = atof(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    while(toggle)
    {
        currentTime = millis();
        Serial.println(power);
        power = Devices::JoystickRead(power);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(power);
            Devices::WriteLCD(str);
        }
        toggle = Devices::JoystickClick();
    }
}

void CommsTask()
{
    // Quickly return if nothing has been received
    if (Serial.available() == 0)
    {

        return;
    }

    // Read the message and determine the request code
    String msg = Serial.readStringUntil('\n');
    RequestCode code = ParseCode(msg);
    String data = ParseData(msg);

    switch (code)
    {
        case RequestCode::INVALID:
            SendResponse(ResponseCode::ERROR);
            break;
        case RequestCode::CHECK:
            SendResponse(ResponseCode::SUCCESS);
            break;
        case RequestCode::HWTRAIN_TOGGLE_CABIN_LIGHTS:
            SetLights(data);
            GetLights(data);
            break;
        case RequestCode::HWTRAIN_PRESS_SERVICE_BRAKE:
            SetBrake(data);
            GetBrake(data);
            break;
        case RequestCode::HWTRAIN_ANNOUNCE_STATIONS:
            SetAnnounce(data);
            GetAnnounce(data);
            break;
        case RequestCode::HWTRAIN_PULL_EBRAKE:
            SetEBrake(data);
            GetEBrake(data);
            break;
        case RequestCode::HWTRAIN_BRAKE_FAILURE:
            SetBrakeFailure(data);
            GetBrakeFailure(data);
            break;
        case RequestCode::HWTRAIN_ENGINE_FAILURE:
            SetEngineFailure(data);
            GetEngineFailure(data);
            break;
        case RequestCode::HWTRAIN_SIGNAL_FAILURE:
            SetSignalFailure(data);
            GetSignalFailure(data);
            break;
        case RequestCode::HWTRAIN_PULL_PASSENGER_EBRAKE:
            SetPEBrake(data);
            GetPEBrake(data);
            break;
        case RequestCode::HWTRAIN_TOGGLE_DAMN_DOORS:
            SetDoors(data);
            GetDoors(data);
            break;
        case RequestCode::HWTRAIN_DISPLAY_ADS:
            SetAds(data);
            GetAds(data);
            break;
        case RequestCode::HWTRAIN_SET_TEMPERATURE:
            DisplayTemp(data);
            break;
        case RequestCode::HWTRAIN_UPDATE_CURRENT_SPEED:
            DisplaySpeed(data);
            break;
        case RequestCode::HWTRAIN_GUI_DISPLAY_POWER:
            DisplayPower(data);
            break;
        case RequestCode::HWTRAIN_GUI_SET_KP:
            DisplayKp(data);
            break;
        case RequestCode::HWTRAIN_GUI_SET_KI:
            DisplayKi(data);
            break;
        default:
            // We expect ParseCode to take care of this case
            assert(false);
    }
}

}