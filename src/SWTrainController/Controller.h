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
        int speed_limit;
        int power_command;
        int authority;
        bool mode;
        bool serviceBrake;
        bool emergencyBrake;

        // Train Engineer inputs
        int kp;
        int ki;

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
         * @param sp_lim = speed limit
         * @param auth = authority
         */
        Controller(int com_sp, int curr_sp, int sp_lim, int auth);

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
         * @param input_speed = speed train driver inputs if train is in manual mode
         */
        void regulateSpeed(int input_speed);

        /**
         * @brief safety critical aspect to stop train immediately
         */
        void activateEmergencyBrake();
        
        /**
         * @brief allows operator to switch between manual and automatic mode
         * @param override = string code entered by operator to initiate manual override
         */
        void toggleMode(std::string override);

        ///////////////////////////////////////////////////////////////
        // NON-VITAL OPERATIONS
        ///////////////////////////////////////////////////////////////
        /**
         * @brief open/close doors
         */
        void toggleDoors();
        /**
         * @brief turn lights on/off
         */
        void toggleLights();
        /**
         * @brief turn announcements on/off
         */
        void announceStations();
        /**
         * @brief turn advertisements on/off
         */
        void toggleAds();
        /**
         * @brief turn air-conditioning on/off
         */
        void toggleAirConditioning();

};
#endif