/**
 * @file ArduinoLogger.hpp
*/
#ifndef ARDUINO_LOGGER_HPP
#define ARDUINO_LOGGER_HPP

// SYSTEM INCLUDES
#include <Arduino.h>

// C++ PROJECT INCLUDES
// (None)

// MACROS
#ifdef DEBUGENABLE
#define LOG(msg) Serial.print(msg)
#define LOGN(msg) Serial.println(msg)
#define LOG_DEC(num) Serial.print((long)num, DEC)
#define LOG_DECN(num) Serial.println((long)num, DEC)
#else
#define LOG(msg)
#define LOGN(msg)
#define LOG_DEC(num)
#define LOG_DECN(num)
#endif

#endif // ARDUINO_LOGGER_HPP
