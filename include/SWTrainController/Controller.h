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
        int command_speed;
        int current_speed;
        int setpoint_speed;
        int power_command;
        bool authority;
        bool mode; // 0 = Automatic, 1 = Manual
        bool serviceBrake;
        bool emergencyBrake;

        // Train Engineer inputs
        int kp;
        int ki;

        // Variables for power calculation
        int uk;
        int uk1;
        int ek;
        int ek1;

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
        Controller(int com_sp, int curr_sp, bool auth);

        ///////////////////////////////////////////////////////////////
        // SETTERS AND GETTERS
        ///////////////////////////////////////////////////////////////

        /**
         * @brief Setter function for Kp
         * @param KP = kp
         */
        void setKp(int KP);

        /**
         * @brief Setter function for Ki
         * @param KI = ki
         */
        void setKi(int KI);

        /**
         * @brief Setter function for command speed
         * @param com_sp == command_speed
         */
        void setCommandSpeed(int com_sp);

        /**
         * @brief Setter function for current speed
         * @param curr_sp == current_speed
         */
        void setCurrentSpeed(int curr_sp);

        /**
         * @brief Setter function for setpoint speed
         * @param setp_sp == setpoint speed
         */
        void setSetpointSpeed(int setp_sp);

        /**
         * @brief Setter function for authority
         * @param auth == authority
         */
        void setAuthority(bool auth);

        /**
         * @brief Getter function for command speed
         * @return command_speed
         */
        int getCommandSpeed();

        /**
         * @brief Getter function for current speed
         * @return current_speed
         */
        int getCurrentSpeed();

        /**
         * @brief Getter function for setpoint speed
         * @return setpoint speed
         */
        int getSetpointSpeed();

        /**
         * @brief Getter function for authority
         * @return authority
         */
        bool getAuthority();

        /**
         * @brief Getter function for power command
         */
        int getPowerCommand();

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
        void setCabinTemp(int temp);
        /**
         * @brief gets temperature of train cabin
         * @return returns temperature of cabin
         */
        int getCabinTemp();

};
#endif