#ifndef TAG_DATABASE_HPP
#define TAG_DATABASE_HPP

#include <string>

using namespace std;

namespace TagDatabase
{
    void AddTag(const char* pTagName);

    bool setTag(const string& rTagName, bool value);

    bool getTagValue(const string& rTagName, bool& rValue);

    void Clear();
}
#endif