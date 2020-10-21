#include "Distance.cpp"
#include "Insidetrain.cpp"
#include "Failures.cpp"
#include "Speedstuff.cpp"
#include "Trainfunctions.cpp"
#include <iostream>
#include <string.h>
#include "Assert.hpp" // For ASSERT
#include "Logger.hpp" // For LOG macros
using namespace std;

int main(){
    // If button is pressed to change doors or lights or what have you, then if it is a bool, the main will change said bool value automatically whereas if it is an int then the user would
    // use the joystick to change the value to whatever they deem fit.
    // For button presses, I will be using a remote with an IR sensor attached to the arduino. 

    
    //LOG_HW_TRACK_CONTROLLER("Thread starting...");

    // while (true)
    // {
    //     Common::Request receivedRequest = serviceQueue.Pop();

    //     switch (receivedRequest.GetRequestCode())
    //     {
    //         case Common::RequestCode::SWTRACK_GET_TRACK_SIGNAL:
    //         {
                
    //             break;
    //         }
    //         default:
    //             ASSERT(false, "Unexpected request received %d", static_cast<uint16_t>(receivedRequest.GetRequestCode()));
    //             break;
    //     }
    // }



    return 0;
}