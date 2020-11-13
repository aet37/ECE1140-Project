/**
 * @file SWTrainControllerMain.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "SWTrainControllerMain.hpp" // Header for functions
#include "HWTrainControllerMain.hpp"
#include "Timekeeper.hpp" // For Timekeeper
#include "TrainModelMain.hpp"
#include "Logger.hpp" // For LOG macros
#include "Assert.hpp"
#include "ControlSystem.h"

namespace SWTrainController
{

Common::ServiceQueue<Common::Request> serviceQueue;

void moduleMain()
{
    LOG_SW_TRAIN_CONTROLLER("Thread starting...");

    // Add a periodic timer for the power loop
    Common::Timekeeper::GetInstance().AddPeriodicTimer(Common::Timekeeper::SAMPLING_PERIOD_IN_MS, &serviceQueue);

    while(true)
    {
        Common::Request req = serviceQueue.Pop();
        switch(req.GetRequestCode())
        {  
            case Common::RequestCode::SWTRAIN_DISPATCH_TRAIN:
            {
                LOG_SW_TRAIN_CONTROLLER("SWTRAIN_DISPATCH_TRAIN received %s", req.GetData().c_str());
                uint32_t trainID = req.ParseData<uint32_t>(0);
                float command_speed = req.ParseData<float>(1);
                float current_speed = req.ParseData<float>(2);
                bool authority = req.ParseData<bool>(3);
                ControlSystem::getInstance().createNewController(command_speed, current_speed, authority);
                // std::string trainIDString = std::to_string(trainID);
                // std::string command_speedString = std::to_string(command_speed)
                // std::string current_speedString = std::to_string(current_speed)
                // std::string authorityString = std::to_string(auth)
                // Common::Request newRequest(Common::RequestCode::HWTRAIN_DISPATCH_TRAIN);
                //newRequest.AppendData(trainIDString);
                //newRequest.AppendData(command_speedString);
                //newRequest.AppendData(current_speedString);
                // TrainControllers.createNewController(com_sp, curr_sp, auth);
                // HWTrainController::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController dispatch train %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS:
            {
                // Read train ID
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Get controller instance to toggle lights
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                // THIS IS WHAT COLLIN HAD BEFORE THE CRASH
                uint32_t lightStatus = tempController->toggleLights();
                std::string trainIDString = std::to_string(trainID);
                std::string lightStatusString = std::to_string(lightStatus);
                // Create new request and send to Train Model
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_LIGHTS);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(lightStatusString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController lights: %d", lightStatus);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_TOGGLE_DAMN_DOORS:
            {
                // Read train ID
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Get controller instance to toggle doors
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                // Get boolean to represent doors and convert info to string
                uint32_t doorStatus = tempController->toggleDoors();
                std::string trainIDString = std::to_string(trainID);
                std::string doorStatusString = std::to_string(doorStatus);
                // Create new request and send to Train Model
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_DOORS);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(doorStatusString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController doors: %d", doorStatus);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_ANNOUNCE_STATIONS:
            {
                // Read train ID
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Get controller instance to toggle announcements
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                // Get boolean to represent announcements and convert info to string
                uint32_t announcementStatus = tempController->announceStations();
                std::string trainIDString = std::to_string(trainID);
                std::string announcementStatusString = std::to_string(announcementStatus);
                // Create new request and send to Train Model
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_ANNOUNCE_STATIONS);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(announcementStatusString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController announcements: %d", announcementStatus);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_DISPLAY_ADS:
            {
                // Read train ID
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Get controller instance to toggle advertisements
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                // Get boolean to represent advertisements and convert info to string
                uint32_t adsStatus = tempController->toggleAds();
                std::string trainIDString = std::to_string(trainID);
                std::string adsStatusString = std::to_string(adsStatus);
                // Create new request and send to Train Model
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_ADS);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(adsStatusString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController advertisements: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_SET_SEAN_PAUL:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                float temperature = req.ParseData<float>(1);
                // Get controller instance to set temperature
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                tempController->setCabinTemp(temperature);
                std::string trainIDString = std::to_string(trainID);
                std::string tempStatusString = std::to_string(temperature);
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_SEAN_PAUL);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(tempStatusString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController current temperature: %d", temperature);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_SWITCH_MODE:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);

                // std::string passcode = req.ParseData<std::string>(1);
                std::string passcode = "override"; // HARDCODED PASSWORD!!!

                // Get controller instance and toggle mode
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                uint32_t modeStatus = tempController->toggleMode(passcode);
                std::string trainIDString = std::to_string(trainID);
                std::string modeStatusString = std::to_string(modeStatus);
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_MODE);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(modeStatusString);
                // TrainModel::serviceQueue.Push(newRequest); Not shown on kenny's gui atm
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController mode: %d", modeStatus);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_SET_SETPOINT_SPEED:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                uint32_t setpoint_speed = req.ParseData<uint32_t>(1);
                // Get controller instance and set setpoint speed
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                tempController->setSetpointSpeed(setpoint_speed);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController setpoint speed: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_PRESS_SERVICE_BRAKE:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                // Get controller instance and toggle service brake
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                bool brakeStatus = tempController->toggleServiceBrake();
                // Create new request and send trainID and brakeStatus as strings
                std::string trainIDString = std::to_string(trainID);
                std::string brakeStatusString = std::to_string(brakeStatus);
                Common::Request newRequest(Common::RequestCode::TRAIN_MODEL_GUI_RECEIVE_SERVICE_BRAKE);
                newRequest.AppendData(trainIDString);
                newRequest.AppendData(brakeStatusString);
                TrainModel::serviceQueue.Push(newRequest);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController service brake: %d", trainID);
                break;
            }
            case Common::RequestCode::SWTRAIN_GUI_SET_KP_KI:
            {
                uint32_t trainID = req.ParseData<uint32_t>(0);
                float kp = req.ParseData<float>(1);
                float ki = req.ParseData<float>(2);
                // Get controller instance to set kp and ki
                Controller* tempController = ControlSystem::getInstance().getControllerInstance(trainID - 1);
                tempController->setKp(kp);
                tempController->setKi(ki);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController Train ID: %d", trainID);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController kp: %d", kp);
                LOG_SW_TRAIN_CONTROLLER("SWTrainController ki: %d", ki);
                break;
            }
            case Common::RequestCode::TIMER_EXPIRED:
            {
                int numberOfControllers = ControlSystem::getInstance().getAmountofControllers();
                LOG_SW_TRAIN_CONTROLLER("Timer event received with %d trains", numberOfControllers);

                for (int i = 0; i < numberOfControllers; i++)
                {
                    Controller* pController = ControlSystem::getInstance().getControllerInstance(i);

                    // Calculate the power
                    pController->calculatePower();

                    // Construct a request to send Kenneth power
                    Common::Request newReq(Common::RequestCode::TRAIN_MODEL_RECEIVE_POWER);
                    newReq.AppendData(std::to_string(i + 1));
                    newReq.AppendData(std::to_string(pController->getPowerCommand()));
                    TrainModel::serviceQueue.Push(newReq);
                }

                break;
            }
            case Common::RequestCode::SWTRAIN_UPDATE_CURRENT_SPEED:
            {
                LOG_SW_TRAIN_CONTROLLER("SWTRAIN_UPDATE_CURRENT_SPEED received %s", req.GetData().c_str());
                uint32_t trainId = req.ParseData<uint32_t>(0);
                float currentSpeed = req.ParseData<float>(1);

                Controller* pController = ControlSystem::getInstance().getControllerInstance(trainId - 1);
                pController->setCurrentSpeed(currentSpeed);

                break;
            }
            default:
                ASSERT(false, "Unexpected request code %d", static_cast<uint16_t>(req.GetRequestCode()));

        }
    }
}

} // namespace SWTrainController
