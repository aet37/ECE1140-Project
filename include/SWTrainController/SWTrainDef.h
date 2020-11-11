#ifndef SWTRAINDef_H
#define SWTRAINDef_H

#include <string>

// Defines the maximum power of the train engine
const int MAX_POWER = 120; // Units for max power are kW

// Define automatic to manual override password
const std::string password = "override";

// Define sampling period for calculating power
const int T = 0.25;

struct NonVitalOperations
{
    // Variables
    bool doors;
    bool announcements;
    bool lights;
    int temperature;
    bool advertisements;

    // Constructor
    NonVitalOperations()
    {
        doors = 0;
        announcements = 0;
        lights = 0;
        temperature = 0;
        advertisements = 0;
    }
};
#endif