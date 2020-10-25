/**
 * @file SWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrainControllerMain.hpp" // Header for functions
#include "TrainModelMain.hpp"
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"

namespace SWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_SW_TRAIN_CONTROLLER("Thread starting...");

    while(true)
    {
        Common::Request req = serviceQueue.Pop();

        switch(req.GetRequestCode())
        {  
            case Common::RequestCode::SWTRAIN_DISPATCH_TRAIN:
            {
                uint32_t theInt = req.ParseData<uint32_t>(0);
                std::string theIntString = std::to_string(theInt);
                Common::Request newRequest(Common::RequestCode::HWTRAIN_DISPATCH_TRAIN, theIntString);
                SWTrainController::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController dispatch train %s", theIntString.c_str());
                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }
    }
}

} // namespace SWTrainController
