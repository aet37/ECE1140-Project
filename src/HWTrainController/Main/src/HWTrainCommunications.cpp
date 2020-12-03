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
static bool menutoggle=1, toggle=1;
static int menuselect=0;
static int temp=70, speed=0, kp=0, ki=0, power=0; // power is calculated later
unsigned long currentTime, previousTime = 0, currentTime1, previousTime1 = 0;
const long interval = 1000, interval1 = 1500;
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
        // case static_cast<int>(RequestCode::HWTRAIN_PULL_EBRAKE):
        // case static_cast<int>(RequestCode::HWTRAIN_SET_SETPOINT_SPEED):
        // case static_cast<int>(RequestCode::HWTRAIN_PRESS_SERVICE_BRAKE):
        // case static_cast<int>(RequestCode::HWTRAIN_TOGGLE_DAMN_DOORS):
        // case static_cast<int>(RequestCode::HWTRAIN_TOGGLE_CABIN_LIGHTS):
        // case static_cast<int>(RequestCode::HWTRAIN_SET_TEMPERATURE):
        // case static_cast<int>(RequestCode::HWTRAIN_ANNOUNCE_STATIONS):
        // case static_cast<int>(RequestCode::HWTRAIN_DISPLAY_ADS):
        case static_cast<int>(RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST):
        case static_cast<int>(RequestCode::HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE):
        case static_cast<int>(RequestCode::HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE):
        // case static_cast<int>(RequestCode::HWTRAIN_DISPATCH_TRAIN):
        // case static_cast<int>(RequestCode::HWTRAIN_UPDATE_CURRENT_SPEED):
        // case static_cast<int>(RequestCode::HWTRAIN_UPDATE_COMMAND_SPEED):
        // case static_cast<int>(RequestCode::HWTRAIN_UPDATE_AUTHORITY):
        // case static_cast<int>(RequestCode::HWTRAIN_SIGNAL_FAILURE):
        // case static_cast<int>(RequestCode::HWTRAIN_PULL_PASSENGER_EBRAKE):
        // case static_cast<int>(RequestCode::HWTRAIN_GUI_GATHER_DATA):
        // case static_cast<int>(RequestCode::HWTRAIN_ENGINE_FAILURE):
        // case static_cast<int>(RequestCode::HWTRAIN_GUI_SET_KP):
        // case static_cast<int>(RequestCode::HWTRAIN_GUI_GET_MODE):
        // case static_cast<int>(RequestCode::HWTRAIN_GUI_DISPLAY_POWER):
        // case static_cast<int>(RequestCode::HWTRAIN_GUI_SET_KI):
        // case static_cast<int>(RequestCode::HWTRAIN_BRAKE_FAILURE):
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
    String str;
    while(1){
        bool whiletoggle = Devices::ButtonClick();
        currentTime1 = millis();
        if (currentTime1 - previousTime1 >= interval1) {
            previousTime1 = currentTime1;       
            menudata = Devices::JoystickRead(menudata);
            if(menudata==14){
                menudata=0;
            } else if(menudata==-1){
                menudata=13;
            }
            if(menudata==0){ // EBrake
                str="Select EBrake";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==1){ // Service Brake
                str="Select Service Brake";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==2){ // Doors
                str="Select Doors";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==3){ // Lights
                str="Select Lights";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
            }
            if(menudata==4){ // Ads
                str="Select Ads";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==5){ // Announce
                str="Select Announcements";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==6){ // Signal Failure
                str="Select Signal Failure";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==7){ // Engine Failure
                str="Select Engine Failure";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==8){ // Brake Failure
                str="Select Brake Failure";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==9){ // Temperature
                str="Select Temperature";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==10){ // Speed
                str="Select Speed";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==11){ // Kp
                str="Select Kp";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==12){ // Ki
                str="Select Ki";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
            if(menudata==13){ // Power
                str="Select Power";
                Devices::ClearLCD();
                Devices::WriteLCD(str);
                
                if(whiletoggle){
                    break;
                }
            }
        }
        if(whiletoggle){
            return menudata;
            break;
        }
    }
    return menudata;
}

static void GetLights()
{

    if(Devices::JoystickClick()){
        lights = !lights;
    }
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

static void GetBrake()
{
    if(Devices::JoystickClick()){
        brake = !brake;
    }
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

static void GetAnnounce()
{
    if(Devices::JoystickClick()){
        announce = !announce;
    }
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

static void GetEBrake()
{
    if(Devices::JoystickClick()){
        ebrake = !ebrake;
    }
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

static void GetPEBrake()
{
    if(Devices::JoystickClick()){
        pebrake = !pebrake;
    }
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

static void GetSignalFailure()
{
    if(Devices::JoystickClick()){
        sigfail = !sigfail;
    }
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

static void GetEngineFailure()
{
    if(Devices::JoystickClick()){
        engfail = !engfail;
    }
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

static void GetBrakeFailure()
{
    if(Devices::JoystickClick()){
        brakefail = !brakefail;
    }
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

static void GetDoors()
{
    if(Devices::JoystickClick()){
        doors = !doors;
    }
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
static void GetAds()
{
    if(Devices::JoystickClick()){
        ads = !ads;
    }
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

static void DisplayTemp()
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggletemp = Devices::JoystickClick();
    while(!toggletemp)
    {
        currentTime = millis();
        temp = Devices::JoystickRead(temp);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(temp);
            Devices::WriteLCD(str);
        }
        toggletemp = Devices::JoystickClick();
    }
}



static void DisplaySpeed()
{
    SendResponse(ResponseCode::SUCCESS);
    bool togglespeed = Devices::JoystickClick();
    while(!togglespeed)
    {
        currentTime = millis();
        Serial.println(speed);
        speed = Devices::JoystickReadCharlie(speed);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(speed);
            Devices::WriteLCD(str);
        }
        togglespeed = Devices::JoystickClick();
    }
}

static void DisplayKi()
{
    SendResponse(ResponseCode::SUCCESS);
    bool toggleki = Devices::JoystickClick();
    while(!toggleki)
    {
        currentTime = millis();
        Serial.println(ki);
        ki = Devices::JoystickReadBeta(ki);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(ki);
            Devices::WriteLCD(str);
        }
        toggleki = Devices::JoystickClick();
    }
}

static void DisplayKp()
{
    SendResponse(ResponseCode::SUCCESS);
    bool togglekp = Devices::JoystickClick();
    while(!togglekp)
    {
        currentTime = millis();
        Serial.println(kp);
        kp = Devices::JoystickReadAlpha(kp);
        if (currentTime - previousTime >= interval) {
            previousTime = currentTime;        
            Devices::ClearLCD();
            String str = String(kp);
            Devices::WriteLCD(str);
        }
        togglekp = Devices::JoystickClick();
    }
}

static void DisplayPower()
{
    // Display the power and the setpoint speed

    
    
    
    
    
    
    
    // SendResponse(ResponseCode::SUCCESS);
    // bool togglepower = Devices::JoystickClick();
    // while(!togglepower)
    // {
    //     currentTime = millis();
    //     Serial.println(power);
    //     power = Devices::JoystickRead(power);
    //     if (currentTime - previousTime >= interval) {
    //         previousTime = currentTime;        
    //         Devices::ClearLCD();
    //         String str = String(power);
    //         Devices::WriteLCD(str);
    //     }
    //     togglepower = Devices::JoystickClick();
    // }
}

String get_data(){
    String str="ebrake ";
    str = str + ebrake + " brake " + brake + " doors " + doors + " lights " + lights + " ads " + ads + " announce " + announce + " sigfail " + sigfail + " engfail " + engfail + " brakefail " + brakefail + " temp " + temp + " speed " + speed + " kp " + kp + " ki " + ki + " power " + power;
    // LOOK AT RUBRIC
    // Just get lights working first
    // Write a function that gets the data and puts it in a string.
    // How to pull data from arduino to python. Pull data from arduino into formatted string that can be parsed through to find variables. "lights 1 doors 0" (formatted as a dictionary)
    // Check to see if data was different than before, if it is then tell kenny that something has been changed (already done in the python file)
    return str;
}

void CommsTask()
{
    
    menuselect = Menu(menuselect);
    
    // Read the message and determine the request code
    //SendResponse(ResponseCode::SUCCESS); // Send data in a string. Ex: lights 1 doors 0 ads 1 etc.)
    
    switch(menuselect)
    {
        case 0: // EBrake
             while(1){
                toggle = Devices::ButtonClick();
                GetEBrake();
                if(toggle){
                    break;
                }
            }
            break;
        case 1: // Service Brake
             while(1){
                toggle = Devices::ButtonClick();
                GetBrake();
                if(toggle){
                    break;
                }
            }
            break;
        case 2: // Doors
             while(1){
                toggle = Devices::ButtonClick();
                GetDoors();
                if(toggle){
                    break;
                }
            }
            break;
        case 3: // Lights
            while(1){
                toggle = Devices::ButtonClick();
                GetLights();
                if(toggle){
                    break;
                }
            }
            // Figure out how to change the code number to 248 so that I can send the data over to kenny
            break;
        case 4: // Ads
             while(1){
                toggle = Devices::ButtonClick();
                GetAds();
                if(toggle){
                    break;
                }
            }
            break;
        case 5: // Announce
             while(1){
                toggle = Devices::ButtonClick();
                GetAnnounce();
                if(toggle){
                    break;
                }
            }
            break;
        case 6: // Signal Failure
             while(1){
                toggle = Devices::ButtonClick();
                GetSignalFailure();
                if(toggle){
                    break;
                }
            }
            break;
        case 7: // Engine Failure
             while(1){
                toggle = Devices::ButtonClick();
                GetEngineFailure();
                if(toggle){
                    break;
                }
            }
            break;
        case 8: // Brake Failure
             while(1){
                toggle = Devices::ButtonClick();
                GetBrakeFailure();
                if(toggle){
                    break;
                }
            }
            break;
        case 9: // Temperature
            DisplayTemp();
            break;
        case 10: // Speed
            DisplaySpeed();
            break;
        case 11: // Kp
            DisplayKp();
            break;
        case 12: // Ki
            DisplayKi();
            break;
        case 13: // Power and speed
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
    // print out to LCD screen

    // parse whatever's on serial port using parse data
    // if it's get all data request (via the code variable), then send all data back
    // I already have the power loop as child class
    String msg = Serial.readStringUntil('\n');
    RequestCode code = ParseCode(msg);
    Devices::ClearLCD();
    Devices::WriteLCD(msg);
    if(code==RequestCode::HWTRAIN_GET_DATA){
        String stri = get_data(); // used to send data over to the python code
        SendResponse(ResponseCode::SUCCESS, stri.c_str());
    }
}

}