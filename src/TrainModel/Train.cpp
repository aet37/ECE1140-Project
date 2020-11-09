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
    m_commandSpeed = 0;
    m_currentSpeed = 0; // THIS IS CALCULATED
    m_position = 0; // THIS IS CALCULATED
    m_authority = 0;
    m_currentBlock = 0;
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
    m_trainLength = 0;
    m_trainWidth = 0;
    m_trainHeight = 0;
    m_trainMass = 0;
    m_trainCrewCount = 0;
    m_trainPassCount = 0;

    // Failure cases
    m_signalPickupFailure = false;
    m_engineFailure = false;
    m_brakeFailure = false;

    // MISC.
    m_mode = false;  // Auto or Manuel
}

} // namespace TrainModel
