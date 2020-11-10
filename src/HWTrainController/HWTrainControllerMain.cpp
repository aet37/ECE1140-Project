/**
 * @file HWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrainControllerMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"
#include "Failures.h"
#include "Distance.h"
#include "Speedstuff.h"
#include "Trainfunctions.h"

namespace HWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_HW_TRAIN_CONTROLLER("Thread starting...");
    Failures Fail;
    Distance Dist;
    Speedstuff Spood;
    Trainfunctions Train;
    while (true)
    {
        Common::Request req = serviceQueue.Pop();

        switch(req.GetRequestCode())
        {
            case Common::RequestCode::HWTRAIN_DISPATCH_TRAIN:
            {
                uint32_t theInt = req.ParseData<uint32_t>(0);
                std::string theIntString = std::to_string(theInt);
                Common::Request newRequest(Common::RequestCode::HWTRAIN_DISPATCH_TRAIN, theIntString);
                LOG_HW_TRAIN_CONTROLLER("HWTrain model dispatch train %s", theIntString.c_str());
                break;
            }
            case Common::RequestCode::HWTRAIN_UPDATE_CURRENT_SPEED:
            {
                Spood
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }


    }


}

// send message to server, using send message function (send message with a request, goes to server, then the request manager picks it up and pushes it on to the queue for hardware)

} // namespace HWTrainController
