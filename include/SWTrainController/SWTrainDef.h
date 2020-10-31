#ifndef SWTRAINDef_H
#define SWTRAINDef_H

// Defines the maximum power of the train engine
const int MAX_POWER = 120; // Units for max power are kW

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