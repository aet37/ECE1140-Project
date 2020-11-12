//
// Created by Collin Hough on 10.7.20
// Defines controller to be used on each train in system
//

#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "SWTrainDef.h"
#include <string>

class Controller
{
    private:
        // Safety critical information
        float command_speed;
        float current_speed;
        float setpoint_speed;
        float power_command;
        bool authority;
        bool mode; // 0 = Automatic, 1 = Manual
        bool serviceBrake;
        bool emergencyBrake;

        // Train Engineer inputs
        float kp;
        float ki;

        // Variables for power calculation
        float uk;
        float uk1;
        float ek;
        float ek1;

        // Failure cases
        bool signalPickupFailure;
        bool engineFailure;
        bool brakeFailure;

        // Struct which holds all non-vital operations
        NonVitalOperations NVO;

    public:
        /**
         * @brief initialize variables
         */
        Controller();

        /** 
         * @brief initializes data coming from train model
         * @param com_sp = command speed
         * @param curr_sp = current speed
         * @param auth = authority
         */
        Controller(float com_sp, float curr_sp, bool auth);

        ///////////////////////////////////////////////////////////////
        // SETTERS AND GETTERS
        ///////////////////////////////////////////////////////////////

        /**
         * @brief Setter function for Kp
         * @param KP = kp
         */
        void setKp(float KP);

        /**
         * @brief Setter function for Ki
         * @param KI = ki
         */
        void setKi(float KI);

        /**
         * @brief Setter function for command speed
         * @param com_sp == command_speed
         */
        void setCommandSpeed(float com_sp);

        /**
         * @brief Setter function for current speed
         * @param curr_sp == current_speed
         */
        void setCurrentSpeed(float curr_sp);

        /**
         * @brief Setter function for setpoint speed
         * @param setp_sp == setpoint speed
         */
        void setSetpointSpeed(float setp_sp);

        /**
         * @brief Setter function for authority
         * @param auth == authority
         */
        void setAuthority(bool auth);

        /**
         * @brief Getter function for command speed
         * @return command_speed
         */
        float getCommandSpeed();

        /**
         * @brief Getter function for current speed
         * @return current_speed
         */
        float getCurrentSpeed();

        /**
         * @brief Getter function for setpoint speed
         * @return setpoint speed
         */
        float getSetpointSpeed();

        /**
         * @brief Getter function for authority
         * @return authority
         */
        bool getAuthority();

        /**
         * @brief Getter function for power command
         */
        float getPowerCommand();

        /**
         * @brief Getter function for mode
         */
        bool getMode();

        /**
         * @brief Getter function for service brake
         */
        bool getServiceBrake();

        // NON-VITAL GETTERS
        /**
         * @brief open/close doors
         */
        bool getDoors();

        /**
         * @brief turn lights on/off
         */
        bool getLights();

        /**
         * @brief turn announcements on/off
         */
        bool getAnnounceStations();

        /**
         * @brief turn advertisements on/off
         */
        bool getAds();

        ///////////////////////////////////////////////////////////////
        // VITAL OPERATIONS
        ///////////////////////////////////////////////////////////////
        /**
         * @brief calculates power command that will be sent to train model
         */
        void calculatePower();

        /**
         * @brief ensures train does not exceed speed limit
         * @brief if train is in automatic mode, speed is set to command speed
         * @brief if train is in manual mode, speed is set to setpoint speed
         */
        void regulateSpeed();

        /**
         * @brief safety critical aspect to stop train immediately
         */
        void activateEmergencyBrake();

        /**
         * @brief safety critical aspect to reset emergency brake
         */
        void resetEmergencyBrake();

        /**
         * @brief toggle service brake on and off
         */
        bool toggleServiceBrake();
        
        /**
         * @brief allows operator to switch between manual and automatic mode
         * @param override = string code entered by operator to initiate manual override
         * @return returns boolean value to signify if override was successful
         */
        bool toggleMode(std::string override);

        ///////////////////////////////////////////////////////////////
        // NON-VITAL OPERATIONS
        ///////////////////////////////////////////////////////////////
        /**
         * @brief open/close doors
         */
        bool toggleDoors();
        /**
         * @brief turn lights on/off
         */
        bool toggleLights();
        /**
         * @brief turn announcements on/off
         */
        bool announceStations();
        /**
         * @brief turn advertisements on/off
         */
        bool toggleAds();
        /**
         * @brief sets temperature of train cabin
         * @param temp = temperature cabin is set to
         */
        void setCabinTemp(float temp);
        /**
         * @brief gets temperature of train cabin
         * @return returns temperature of cabin
         */
        float getCabinTemp();

};
#endif