#include <assert.h>
#include <Arduino.h>

#include "../include/HWTrainCommunications.hpp"
#include "../include/Devices/Devices.hpp"

namespace HWTrainCommunications
{
// Determines the request code
static bool lights;
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
        case static_cast<int>(RequestCode::HWTRAIN_CAUSE_FAILURE):
        case static_cast<int>(RequestCode::HWTRAIN_PULL_PASSENGER_EBRAKE):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_GATHER_DATA):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_RESOLVE_FAILURE):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_SET_KP):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_GET_MODE):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_DISPLAY_POWER):
        case static_cast<int>(RequestCode::HWTRAIN_GUI_SET_KI):


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
    // Parse the message between tag name and value
    //lights = atoi(rData.substring(rData.indexOf(" "), rData.length()).c_str());
    lights = atoi(rData.substring(rData.indexOf(" ")+1, rData.length()).c_str());
    Serial.print("Lights: ");
    Serial.print(lights);
    Serial.print("\n");
    digitalWrite(LED_BUILTIN, lights ? HIGH : LOW);
    SendResponse(ResponseCode::SUCCESS);
}

static void GetLights(const String& rData)
{
    SendResponse(ResponseCode::SUCCESS, lights ? "1" : "0");
    if(lights==1)
    {
        Devices::WriteCharLCD("Lights are on");
    } else {
        Devices::WriteCharLCD("Lights are off");
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
        
        default:
            // We expect ParseCode to take care of this case
            assert(false);
    }
}

}