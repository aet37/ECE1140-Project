#include <assert.h>
#include <Arduino.h>

#include "../include/HWTrainCommunications.hpp"
#include "../include/Devices/Devices.hpp"

// Get stuff to show up on Kenny's GUI

namespace HWTrainCommunications
{
static bool lights=0;
static bool brake=1; // On until kp and ki are set
static bool ebrake=0;
static bool doors=0;
static bool announce=0;
static bool pebrake=0;
static bool sigfail=0, engfail=0, brakefail=0;
static bool ads=0;
static double temp=70, speed=0, kp=0, ki=0, power=0; // power is calculated later
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
        case static_cast<int>(RequestCode::HWTRAIN_GET_DATA):


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

int Menu(int menudata){
    bool toggle;
    String str;
    while(1){
        toggle = Devices::ButtonClick();
        currentTime = millis();
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            menudata = Devices::JoystickRead(menudata);
            if(menudata==15){
                menudata=0;
            } else if(menudata==-1){
                menudata=14;
            }
            Serial.println(menudata);
            if(menudata==0){ // EBrake
                str="Select EBrake";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                Serial.println(toggle);
            }
            if(menudata==1){ // Service Brake
                str="Select Service Brake";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==2){ // Passenger EBrake
                str="Select Passenger EBrake";
                Devices::ClearLCD();  
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==3){ // Doors
                str="Select Doors";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==4){ // Lights
                str="Select Lights";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==5){ // Ads
                str="Select Ads";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==6){ // Announce
                str="Select Announcements";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==7){ // Signal Failure
                str="Select Signal Failure";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==8){ // Engine Failure
                str="Select Engine Failure";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==9){ // Brake Failure
                str="Select Brake Failure";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==10){ // Temperature
                str="Select Temperature";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==11){ // Speed
                str="Select Speed";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==12){ // Kp
                str="Select Kp";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==13){ // Ki
                str="Select Ki";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
            if(menudata==14){ // Power
                str="Select Power";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(toggle){
                    break;
                }
            }
        }
        Serial.print("While loop end\n");
        if(toggle){
            return menudata;
            break;
        }
    }
    Serial.print("We out\n");
    return menudata;
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
    while(!toggle)
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
    while(!toggle)
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
    while(!toggle)
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
    while(!toggle)
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

String get_data(){
    // Write a function that gets the data and puts it in a string.
    // How to pull data from arduino to python. Pull data from arduino into formatted string that can be parsed through to find variables. "lights 1 doors 0"
    // Check to see if data was different than before, if it is then tell kenny that something has been changed
}

void CommsTask()
{
    Serial.print("Beginning");
    Serial.print("Before call");
    int menuselect = Menu(0);
    Serial.print("After call");

    // Read the message and determine the request code
    String msg = Serial.readStringUntil('\n');
    RequestCode code = ParseCode(msg);
    SendResponse(ResponseCode::SUCCESS, // Send data in a string. Ex: lights 1 doors 0 ads 1 etc.)
    switch(menuselect)
    {
        case 0: // EBrake
            SetEBrake();
            GetEBrake();
            break;
        case 1: // Service Brake
            SetBrake();
            GetBrake();
            break;
        case 2: // Passenger EBrake
            SetPEBrake();
            GetPEBrake();
            break;
        case 3: // Doors
            SetDoors();
            GetDoors();
            break;
        case 4: // Lights
            SetLights();
            GetLights();
            break;
        case 5: // Ads
            SetAds();
            GetAds();
            break;
        case 6: // Announce
            SetAnnounce();
            GetAnnounce();
            break;
        case 7: // Signal Failure
            SetSignalFailure();
            GetSignalFailure();
            break;
        case 8: // Engine Failure
            SetEngineFailure();
            GetEngineFailure();
            break;
        case 9: // Brake Failure
            SetBrakeFailure();
            GetBrakeFailure();
            break;
        case 10: // Temperature
            DisplayTemp();
            break;
        case 11: // Speed
            DisplaySpeed();
            break;
        case 12: // Kp
            DisplayKp();
            break;
        case 13: // Ki
            DisplayKi();
            break;
        case 14: // Power
            DisplayPower();
            break;
        default: 
            break;

    }

    // Quickly return if nothing has been received
    if (Serial.available() == 0)
    {
        return;
    }

    // parse whatever's on serial port using parse data
    // if it's get all data request (via the code variable), then send all data back
    // I already have the power loop as child class
    if(code==RequestCode::HWTRAIN_GET_DATA){
        string stri = get_data(); // used to send data over to the python code
    }
}

}