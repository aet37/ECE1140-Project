#ifndef SWTRAINDef_H
#define SWTRAINDef_H

struct NonVitalOperations
{
    // Variables
    bool doors;
    bool announcements;
    bool lights;
    bool airConditioning;
    bool advertisements;

    // Constructor
    NonVitalOperations()
    {
        doors = 0;
        announcements = 0;
        lights = 0;
        airConditioning = 0;
        advertisements = 0;
    }
};
#endif