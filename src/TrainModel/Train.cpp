/**
 * @file Train.cpp
 *
 * @author Kenny Meier
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Train.hpp" // Header for class

namespace TrainModel
{

Train::Train()
{
    // Initialize vital variables

    // INTEGERS (Vital)
    m_destinationBlock = 0;
    m_commandSpeed = 0;
    m_currentSpeed = 0; // THIS IS CALCULATED
    m_position = 0; // THIS IS CALCULATED
    m_authority = 0;
    m_currentLine = 0; // Default green line
    m_power = 0;
    // INTEGERS (Nonvital)
    m_tempControl = 0;

    // BOOLEANS (Vital)
    m_emergencyPassengeBrake = false;
    m_serviceBrake = false;
    m_brakeCommand = false;
    // BOOLEANS (Nonvital)
    m_headLights = false;
    m_cabinLights = false;
    m_advertisements = false;
    m_announcements = false;
    m_doors = false;

    // Parameter Inputs
    m_trainLength = 32.2; // Meters
    m_trainWidth = 2.65; // Meters
    m_trainHeight = 3.42; // Meters
    m_trainMass = 40.9; // Tons
    m_trainCrewCount = 0;
    m_trainPassCount = 2; // HARDCODED (Unless told otherwise)

    // Failure cases
    m_signalPickupFailure = false;
    m_engineFailure = false;
    m_brakeFailure = false;

    // MISC.
    m_mode = false;  // Auto or Manuel
}

} // namespace TrainModel
