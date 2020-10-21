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
#include <stdint.h>
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
    ERROR = 1,
    DEBUG_TO_CTC = 2,
    DEBUG_TO_HWTRACKCTRL = 3,
    DEBUG_TO_SWTRACKCTRL = 4,
    DEBUG_TO_TRACK_MODEL = 5,
    DEBUG_TO_TRAIN_MODEL = 6,
    DEBUG_TO_HWTRAINCTRL = 7,
    DEBUG_TO_SWTRAINCTRL = 8,

    CTC_DISPATCH_TRAIN = 32,
    CTC_SEND_GUI_OCCUPANCIES = 33,
    CTC_UPDATE_AUTHORITY = 34,
    CTC_UPDATE_SPEED = 35,
    CTC_UPDATE_SIGNAL = 36,
    CTC_UPDATE_SCHEDULE = 37,
    CTC_UPDATE_AUTOMATIC_MODE = 38,
    CTC_UPDATE_SWITCH = 37,
    CTC_SEND_GUI_THROUGHPUT = 38,
    CTC_SEND_GUI_TRAIN_INFO = 39,
    CTC_SEND_GUI_TRACK_INFO = 40,
    CTC_SEND_GUI_SIGNAL_INFO = 41,
    CTC_GET_SIGNALS = 61,
    CTC_GET_TRACK_STATUS = 62,
    CTC_GET_OCCUPANCIES = 63,

    SWTRACK_GET_TRACK_SIGNAL = 64,
    SWTRACK_TRACKSIGNAL_TO_TRAINM = 65,
    SWTRACK_SWITCHPOSITION_TO_TRAINM = 66,
    SWTRACK_GET_OCCUPANCY = 67,
    SWTRACK_GET_SWITCH_POSITION = 68,

    HWTRACK_START_DOWNLOAD = 96,
    HWTRACK_END_DOWNLOAD = 97,
    HWTRACK_CREATE_TAG = 98,
    HWTRACK_CREATE_TASK = 99,
    HWTRACK_CREATE_ROUTINE = 100,
    HWTRACK_CREATE_RUNG = 101,
    HWTRACK_SET_TAG_VALUE = 102,
    HWTRACK_GET_TAG_VALUE = 103,
    HWTRACK_GET_HW_TRACK_CONTROLLER_REQUEST = 104,
    HWTRACK_SEND_HW_TRACK_CONTROLLER_RESPONSE = 105,
    HWTRACK_GET_HW_TRACK_CONTROLLER_RESPONSE = 106,

    GET_SIGNAL_TIMES = 128,
    SET_SPEED_LIMIT = 129,
    GET_SPEED_LIMIT = 130,

    TRAIN_MODEL_GIVE_POWER = 160,
    TRAIN_MODEL_GET_CURRENT_SPEED = 161,
    GET_COMMAND_SPEED = 162,
    SET_TRAIN_LENGTH = 163,
    SEND_TRAIN_MODEL_DATA = 164,

    SEND_TRAIN_MODEL_INFO = 192,
    GET_INFO_FROM_TM = 193,
    SW_TRAIN_CONTROLLER_GET_CURRENT_SPEED = 194,

    HWTRAIN_GET_HW_TRAIN_CONTROLLER_REQUEST = 224,
    HWTRAIN_SEND_HW_TRAIN_CONTROLLER_RESPONSE = 225,
    

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
     * @param idx   Index of the data element you want to retrieve
     * @return Individual data as type T
    */
    template<typename T>
    T ParseData(uint32_t idx) const
    {
        // Check the idx first
        size_t spaceCount = std::count( m_data.begin(), m_data.end(), ' ');
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
