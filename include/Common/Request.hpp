/**
 * @file Request.hpp
 *
 * @brief Data structure to be used to request an action of a module
*/
#ifndef REQUEST_HPP
#define REQUEST_HPP

// SYSTEM INCLUDES
#include <algorithm>
#include <iostream>
#include <string>

// C++ PROJECT INCLUDES
#include "Logger.hpp" // For LOG macros

namespace Common
{

/**
 * @enum RequestCode
 *
 * @brief Codes that will be used when communicating with
 * the server. Each module is assigned a range of numbers
 *
 * @li System wide: 0 - 31
 * @li CTC: 32 - 63
 * @li Software Track Controller: 64 - 95
 * @li Hardware Track Controller: 96 - 127
 * @li Track Model: 128 - 159
 * @li Train Model: 160 - 191
 * @li Software Train Controller: 192 - 223
 * @li Hardware Train Controller: 224 - 255
*/
enum class RequestCode : uint8_t
{
    ERROR = 1, // Used by the system in the case that there was an error parsing the original request
    DEBUG_TO_CTC = 2,
    DEBUG_TO_HWTRACKCTRL = 3,
    DEBUG_TO_SWTRACKCTRL = 4,
    DEBUG_TO_TRACK_MODEL = 5,
    DEBUG_TO_TRAIN_MODEL = 6,
    DEBUG_TO_HWTRAINCTRL = 7,
    DEBUG_TO_SWTRAINCTRL = 8,
    TIMER_EXPIRED = 9, // Used by the timekeeper to tell a module that its timer has expired

    CTC_GUI_DISPATCH_TRAIN = 32, // Used by the gui when the dispatcher dispatches a new train
	CTC_SEND_GUI_GREEN_OCCUPANCIES = 33,
	CTC_SEND_GUI_RED_OCCUPANCIES = 34,
    CTC_UPDATE_AUTHORITY = 35,
    CTC_UPDATE_SPEED = 36,
    CTC_UPDATE_SIGNAL = 37,
    CTC_UPDATE_SCHEDULE = 38,
    CTC_UPDATE_AUTOMATIC_MODE = 39,
    CTC_UPDATE_SWITCH = 40,
    CTC_SEND_GUI_THROUGHPUT = 41, // Used by the track model to give the ctc ticket sales
    CTC_SEND_GUI_TRAIN_INFO = 42,
	CTC_SEND_GUI_SWITCH_POS_GREEN = 43,
	CTC_SEND_GUI_SWITCH_POS_RED = 44,
    CTC_SEND_GUI_SIGNAL_INFO = 45,
    CTC_SEND_TIMER_REQUEST = 46,
    CTC_TIME_TRIGGERED = 60,
    CTC_GET_SIGNALS = 61,
    CTC_GET_SWITCHES = 62,
    CTC_GET_OCCUPANCIES = 63,

    SWTRACK_DISPATCH_TRAIN = 64, // Used by the CTC to signify that a new train has been dispatched // (trainID, destinationBlock, commandSpeed, authority, trackColor, switchPositions)
    SWTRACK_UPDATE_AUTHORITY = 65, // Used by the CTC when a train's authority has been updated
    SWTRACK_SET_TRACK_SIGNAL = 66, // Used by the CTC to set a track block's signal color
    SWTRACK_UPDATE_COMMAND_SPEED = 67, // Used by the CTC when a train's command speed is updated
    SWTRACK_SET_TRACK_STATUS = 68, // Used by the CTC when a block is closed/open for maintenance
    SWTRACK_SET_SWITCH_POSITION = 69, // Used by the CTC when a track switch needs flipped
    SWTRACK_SET_TRACK_FAILURE = 70, // Used by the track model to inform the controller that a failure has occured on a block
    SWTRACK_SET_TRACK_OCCUPANCY = 71, // Used by the track model to inform the controller that a train is on a block // (blockId, trainOrNot)
    SWTRACK_SET_CROSSING = 72, // Used by the track model to have the controller lower/raise the crossing // (blockId, up/down)
    SWTRACK_SET_TRACK_HEATER = 73, // Used by the Track model to turn on/off the track heater // (trackColor, on/off)

    // The following request codes are used by the sw track controller gui to download a plc program
    // An offset is used to convert them to hw track controller requests. PLEASE DON'T CHANGE THE NUMBERS!!!
    START_DOWNLOAD = 74, // Used by the gui to start a download
    END_DOWNLOAD = 75, // Used by the gui to end a download
    CREATE_TAG = 76, // Used by the gui to create a tag
    CREATE_TASK = 77, // Used by the gui to create a task
    CREATE_ROUTINE = 78, // Used by the gui to create a routine
    CREATE_RUNG = 79, // Used by the gui to create a rung
    CREATE_INSTRUCTION = 80, // Used by the gui to create an instruction
    SET_TAG_VALUE = 81, // Used by the gui to set a tag's value
    GET_TAG_VALUE = 82, // Used by the gui to get a tag's value

    SWTRACK_GUI_GATHER_DATA = 83, // Used by the gui to periodically gather data from the server // (trackColor, blockId) // (trackHeater, switchPosition, lightStatus, occupied, trackStatus, railwayCrossing, authority, suggestedSpeed, commandSpeed)
    SWTRACK_GUI_SET_SWITCH_POSITION = 84, // Used by the gui to set a switch's position // (trackController, newPosition)

    HWTRACK_START_DOWNLOAD = 96, // Used by the SW Track Ctrl to signify download is starting // (string programName)
    HWTRACK_END_DOWNLOAD = 97, // Used by the SW Track Ctrl to signify download has completed // (void)
    HWTRACK_CREATE_TAG = 98, // Used by the SW Track Ctrl to create a tag in the hardware // (string tagName, bool defaultValue)
    HWTRACK_CREATE_TASK = 99, // Used by the SW Track Ctrl to create a task in the hardware // (string taskType, (float period | string event), string taskName)
    HWTRACK_CREATE_ROUTINE = 100, // Used by the SW Track Ctrl to create a routine in the hardware // (string routineName)
    HWTRACK_CREATE_RUNG = 101, // Used by the SW Track Ctrl to create a rung in the hardware // ((void | string rungName))
    HWTRACK_CREATE_INSTRUCTION = 102, // Used by the SW Track Ctrl to create an instruction in the hardware // (instructionType argument)
    HWTRACK_SET_TAG_VALUE = 103, // Used by the SW Track Ctrl to set a tag value // (string tagName, bool newValue)
    HWTRACK_GET_TAG_VALUE = 104, // Used by the SW Track Ctrl to get a tag value // (string tagName)
    HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST = 105, // Used by the connector script to check if any requests exist for the hardware
    HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE = 106, // Used by the connector script to forward the hardware's response to the server
    HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE = 107, // Used by SW Track Ctrl to get response from the hardware

    TRACK_MODEL_GUI_TRACK_LAYOUT_START = 129, // Used by the gui to signify that the track layout is starting to be sent
    TRACK_MODEL_GUI_TRACK_LAYOUT_END = 130, // Used by the gui to signify that the full track layout has been sent
    TRACK_MODEL_GUI_TRACK_LAYOUT_SECTION = 131, // Used by the gui when the track layout is being imported
    TRACK_MODEL_GUI_SET_TRACK_HEATER = 132, // Used by the gui when the track heater is set
    TRACK_MODEL_GUI_SET_FAILURE = 133, // Used by the gui when a track failure is induced
    TRACK_MODEL_GUI_GATHER_DATA = 134, // Used periodically by the gui to update the user interface
    TRACK_MODEL_GUI_EDIT_BLOCK_LENGTH = 135, // Used by the gui to edit block length
    TRACK_MODEL_GIVE_POSITION = 136, // Used by the train model to give the track model the position of a train // (blockId, trainOrNot)
    TRACK_MODEL_UPDATE_COMMAND_SPEED = 137, // Used by the track controller to update the command speed of a train // (trainId, newSpeed)
    TRACK_MODEL_UPDATE_SWITCH_POSITIONS = 138, // Used by the track controller to update a switch positions // (trackColor, switchNumberFromYard, switchPosition)
    TRACK_MODEL_UPDATE_AUTHORITY = 139, // Used by the track controller to update the authority of a train // (trainId, newAuthority)
    TRACK_MODEL_DISPATCH_TRAIN = 140, // Used by the track controller to signify that a new train has been dispatched // (trainID, destinationBlock, commandSpeed, authority, trackColor)

    TRAIN_MODEL_GUI_GATHER_DATA = 160, // Used periodically by the gui to update the user interface
    TRAIN_MODEL_DISPATCH_TRAIN = 161, // Used by the track model to signify that a new train has been dispatched
    TRAIN_MODEL_UPDATE_AUTHORITY = 162, // Used by the track model to update a train's authority
    TRAIN_MODEL_UPDATE_COMMAND_SPEED = 163, // Used by the track model to update a train's command speed
    TRAIN_MODEL_SET_THE_DAMN_LIGHTS = 164, // Used by the track model to let the train model know that the train is in a tunnel
    TRAIN_MODEL_GIVE_POWER = 165, // Used by the train controller to give the train model a value for power
    TRAIN_MODEL_GUI_CAUSE_FAILURE = 166, // Used by the gui to cause a train failure
    TRAIN_MODEL_GUI_SET_TRAIN_LENGTH = 167, // Used by the gui to set a train's length
    TRAIN_MODEL_GUI_SET_TRAIN_MASS = 168, // Used by the gui to set a train's mass
    TRAIN_MODEL_GUI_SET_TRAIN_HEIGHT = 169, // Used by the gui to set a train's height
    TRAIN_MODEL_GUI_SET_TRAIN_WIDTH = 170, // Used by the gui to set a train's width
    TRAIN_MODEL_GUI_SET_TRAIN_PASSENGER_COUNT = 171, // Used by the gui to set a train's passenger count
    TRAIN_MODEL_GUI_SET_TRAIN_CREW_COUNT = 172, // Used by the gui to set a train's crew count
    TRAIN_MODEL_GUI_UPDATE_DROP_DOWN = 173, // Used by the gui to update the drop-down that contains the trains

    SWTRAIN_DISPATCH_TRAIN = 192, // Used by the train model to signify that a new train has been dispatched
    SWTRAIN_UPDATE_CURRENT_SPEED = 193, // Used by the train model to update a train's current speed
    SWTRAIN_UPDATE_COMMAND_SPEED = 194, // Used by the train model to update a train's command speed
    SWTRAIN_UPDATE_SPEED_LIMIT = 195, // Used by the train model to update a train's speed limit
    SWTRAIN_UPDATE_AUTHORITY = 196, // Used by the train model to update a train's authority
    SWTRAIN_CAUSE_FAILURE = 197, // Used by the train model to cause a train's failure
    SWTRAIN_PULL_PASSENGER_EBRAKE = 198, // Used by the train model to pull a train's passenger e-brake
    SWTRAIN_GUI_GATHER_DATA = 199, // Used by the gui to update the user interface
    SWTRAIN_GUI_PULL_EBRAKE = 200, // Used by the gui to pull the train's ebrake
    SWTRAIN_GUI_SET_SETPOINT_SPEED = 201, // Used by the gui to set a train's setpoint speed
    SWTRAIN_GUI_PRESS_SERVICE_BRAKE = 202, // Used by the gui to update use a train's service brake
    SWTRAIN_GUI_TOGGLE_DAMN_DOORS = 203, // Used by the gui to toggle a train's door
    SWTRAIN_GUI_TOGGLE_CABIN_LIGHTS = 204, // Used by the gui to toggle a train's lights
    SWTRAIN_GUI_SET_SEAN_PAUL = 205, // Used by the gui to play temperature by sean paul
    SWTRAIN_GUI_ANNOUNCE_STATIONS = 206, // Used by the gui to announce stations
    SWTRAIN_GUI_DISPLAY_ADS = 207, // Used by the gui to display a train's advertisements
    SWTRAIN_GUI_RESOLVE_FAILURE = 208, // Used by the gui to resolve a train failure
    SWTRAIN_GUI_SET_KP_KI = 209, // Used by the gui to set a train's kp/ki

    HWTRAIN_PULL_EBRAKE = 224, // Used by the HW Train Ctrl to pull the train's ebrake
    HWTRAIN_SET_SETPOINT_SPEED = 225, // Used by the HW Train Ctrl to set a train's setpoint speed
    HWTRAIN_PRESS_SERVICE_BRAKE = 226, // Used by the HW Train Ctrl to update use a train's service brake
    HWTRAIN_TOGGLE_DAMN_DOORS = 227, // Used by the HW Train Ctrl to toggle a train's door
    HWTRAIN_TOGGLE_CABIN_LIGHTS = 228, // Used by the HW Train Ctrl to toggle a train's lights
    HWTRAIN_SET_TEMPERATURE = 229, // Used by the HW Train Ctrl to play temperature by sean paul
    HWTRAIN_ANNOUNCE_STATIONS = 230, // Used by the HW Train Ctrl to announce stations
    HWTRAIN_DISPLAY_ADS = 231, // Used by the HW Train Ctrl to display a train's advertisements
    HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST = 232, // Used by the connector script to check if any requests exist for the hardware
    HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE = 233, // Used by the connector script to forward the hardware's response to the server
    HWTRAIN_GET_HW_TRAIN_CONTROLLER_RESPONSE = 234, // Used by HW Train Ctrl to get response from the hardware
    HWTRAIN_DISPATCH_TRAIN = 235, // Used by HWTrainController to signify a train has been dispatched
    HWTRAIN_UPDATE_CURRENT_SPEED = 236, // Used by the train model to update a train's current speed
    HWTRAIN_UPDATE_COMMAND_SPEED = 237, // Used by the train model to update a train's command speed
    HWTRAIN_UPDATE_AUTHORITY = 238, // Used by the train model to update a train's authority
    HWTRAIN_CAUSE_FAILURE = 239, // Used by the train model to cause a train's failure
    HWTRAIN_PULL_PASSENGER_EBRAKE = 240, // Used by the train model to pull a train's passenger e-brake
    HWTRAIN_GUI_GATHER_DATA = 241, // Used by the gui to update the user interface
    HWTRAIN_GUI_RESOLVE_FAILURE = 242, // Used by the gui to resolve a train failure
    HWTRAIN_GUI_SET_KP = 243, // Set Kp
    HWTRAIN_GUI_GET_MODE = 244, // Displays the mode
    HWTRAIN_GUI_DISPLAY_POWER = 245, // Displays power
    HWTRAIN_GUI_SET_KI = 246, // Set Ki
};

/**
 * @class Request
 *
 * @brief Structure used to hold the request code and
 * additional data
*/
class Request
{
public:
    /**
     * @brief Constructs a new Request object
    */
    Request(RequestCode reqCode, std::string data) :
        m_reqCode(reqCode),
        m_data(data)
    {}

    Request() :
        Request(RequestCode::ERROR, "")
    {}

    explicit Request(RequestCode reqCode) :
        Request(reqCode, "")
    {}

    /**
     * @brief Sets the response code member
    */
    void SetRequestCode(const RequestCode reqCode) { m_reqCode = reqCode; }

    /**
     * @brief Sets the data string member
    */
    void SetData(const std::string data) { m_data = data; }

	/**
	 * @brief Writes data to the data string member
	*/
	void AppendData(const std::string& rData)
	{
		if (m_data == "")
		{
			m_data = rData;
		}
		else
		{
			m_data += " " + rData;
		}
	}

    /**
     * @brief Parses a single argument within the request's data as a given type
     * 
     *
     * @param idx   Index of the data element you want to retrieve
     * @return Individual data as type T
    */
    template<typename T>
    T ParseData(uint32_t idx) const
    {
        // Check the idx first
        size_t spaceCount = std::count(m_data.begin(), m_data.end(), ' ');
        if (idx > spaceCount)
        {
            LOG_DEBUG("Index is out of bounds");
            throw std::exception();
        }

        uint32_t startingIndex = 0;
        for (int token = 0; token < idx; token++)
        {
            startingIndex = m_data.find(" ", startingIndex + 1) + 1;
        }

        uint32_t endIndex = m_data.find(' ', startingIndex);
        if constexpr (std::is_same<T, std::string>::value)
        {
            return m_data.substr(startingIndex, endIndex);
        }
        else
        {
            return static_cast<T>(std::stoi(m_data.substr(startingIndex, endIndex)));
        }
    }

    /**
     * @brief Gets the data member
    */
    const std::string& GetData() const { return m_data; }

    /**
     * @brief Gets the request code member
    */
    RequestCode GetRequestCode() const { return m_reqCode; }

    /**
     * @brief Converts the object to a single string
    */
    std::string ToString()
    {
        if (m_data == "")
        {
            return std::to_string(static_cast<uint8_t>(m_reqCode));
        }
        else
        {
            return std::to_string(static_cast<uint8_t>(m_reqCode)) + " " + m_data;
        }
    }

protected:
private:
    /// Request code to designate what the request is for
    RequestCode m_reqCode;

    /// Data to go along with request
    std::string m_data;
};

} // namespace Common

#endif // REQUEST_HPP
