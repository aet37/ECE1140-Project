/**
 * @file HWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "HWTrainControllerMain.hpp" // Header for functions
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"

namespace HWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_HW_TRAIN_CONTROLLER("Thread starting...");

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
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }


    }


}

// send message to server, using send message function (send message with a request, goes to server, then the request manager picks it up and pushes it on to the queue for hardware)

} // namespace HWTrainController
