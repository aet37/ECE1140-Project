/**
 * @file TagDatabase.hpp
*/
#ifndef TAG_DATABASE_HPP
#define TAG_DATABASE_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

// FORWARD REFERENCES
class String;

namespace TagDatabase
{

/**
 * @brief Adds a tag and defaults the value
 *
 * @param pTagName     Name of the tag
*/
void AddTag(const char* pTagName);

/**
 * @brief Sets the given tag to true
 *
 * @param rTagName   Name of tag to set
 * @param value      Value to set tag to
 * @return Whether tag was able to be set or not
*/
bool SetTag(const String& rTagName, bool value);

/**
 * @brief Gets a tag's value
 *
 * @param[in] rTagName   Name of the tag
 * @param[out] rValue    Value of the tag
 * @return Whether operation was successful
*/
bool GetTagValue(const String& rTagName, bool& rValue);

/**
 * @brief Deletes all tags from the database
*/
void Clear();

/**
 * @brief Gets all the tag's and their values
*/
String GetAllTagValues();

/**
 * @brief Task to handle input and outputs
 *
 * @param pNothing      This argument is not used
*/
void IoTask(void* pNothing);

} // namespace TagDatabase

#endif // TAG_DATABASE_HPP
