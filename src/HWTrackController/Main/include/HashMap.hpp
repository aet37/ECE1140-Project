/**
 * @file HashMap.hpp
*/
#ifndef HASH_MAP_HPP
#define HASH_MAP_HPP

// SYSTEM INCLUDES
#include <assert.h>
#include <Arduino.h>

// C++ PROJECT INCLUDES
#include "List.hpp" // For List

// Account for compiler differences if unit testing
#ifdef BUILD_UNIT_TEST
#include <string>
#include <cmath>
#define String std::string
#endif

/**
 * @class HashMap
 *
 * @brief HashMap data structure
 * @tparam T Type of values stored
*/
template <typename T>
class HashMap
{
public:
    /**
     * @brief Constructs a new HashMap object
     *
     * @param[in] size Initial size of the hashmap
    */
    explicit HashMap(uint32_t size = 11) :
        m_pKeys(new String[size]),
        m_pValues(new T[size]),
        m_numElements(0),
        m_size(size)
    {}

    /**
     * @brief Destroys a hashmap object
    */
    ~HashMap()
    {
        delete[] m_pKeys;
        delete[] m_pValues;
    }

    /**
     * @brief Inserts an element into the hashmap
     * using the given key
     *
     * @param key       Key at which to insert
     * @param value     Value to associate with key
    */
    void Insert(String key, T value)
    {
        if (m_numElements == m_size)
        {
            Rehash();
        }

        uint32_t hash = CalculateHash(key);
        if (m_pKeys[hash] == "" || m_pKeys[hash] == key)
        {
            m_pKeys[hash] = key;
            m_pValues[hash] = value;
        }
        else
        {
            // Loop around table until an empty spot is found
            uint32_t i;
            for (i = hash + 1; i != hash; i = (i + 1) % m_size)
            {
                if (m_pKeys[i] == "")
                {
                    m_pKeys[i] = key;
                    m_pValues[i] = value;
                    break;
                }
            }
        }
        m_numElements++;
    }

    /**
     * @brief Obtains an element corresponding
     * to the given key
     *
     * @param rKey      Key whose value to retrieve
     * @return Values associated with key
    */
    const T& Get(const String& rKey) const
    {
        uint32_t hash = CalculateHash(rKey);
        if (m_pKeys[hash] == rKey)
        {
            return m_pValues[hash];
        }
        else
        {
            // Loop around table until the key is found
            for (uint32_t i = hash + 1; i != hash; i = (i + 1) % m_size)
            {
                if (m_pKeys[i] == rKey)
                {
                    return m_pValues[i];
                }
            }
        }

        // Assert if the key is not found
        assert(false);
    }

    /**
     * @brief Updates the value associated with the given key
     *
     * @param rKey      Key whose value to update
     * @param newValue  New value for the key
     * @return False if the key isn't found
    */
    bool Update(const String& rKey, T newValue)
    {
        bool updated = false;
        uint32_t hash = CalculateHash(rKey);
        if (m_pKeys[hash] == rKey)
        {
            m_pValues[hash] = newValue;
            updated = true;
        }
        else
        {
            // Loop around table until the key is found
            for (uint32_t i = hash + 1; i != hash; i = (i + 1) % m_size)
            {
                if (m_pKeys[i] == rKey)
                {
                    m_pValues[i] = newValue;
                    updated = true;
                }
            }
        }
        return updated;
    }

    /**
     * @brief Determines if an element exists
     * for the given key
     *
     * @param rKey      Key to look for
     * @return Whether key exists in the hash
     *      @retval true    - Key is in hash
     *      @retval false   - Key is not in hash
    */
    bool Contains(const String& rKey) const
    {
        uint32_t hash = CalculateHash(rKey);
        if (m_pKeys[hash] == rKey)
        {
            return true;
        }
        else
        {
            // Loop around table until the key is found
            for (uint32_t i = hash + 1; i != hash; i = (i + 1) % m_size)
            {
                if (m_pKeys[i] == rKey)
                {
                    return true;
                }
            }
        }
        return false;
    }

protected:
private:
    /// Array to store keys
    String* m_pKeys;

    /// Array to store values
    T* m_pValues;

    /// Number of elements that were added
    uint32_t m_numElements;

    /// Size of HashMap
    uint32_t m_size;

    /**
     * Calculates the index of the string using
     * Horner's method
     *
     * @param rStr      String to be hashed
     * @return          Hash of the string
    */
    uint32_t CalculateHash(const String& rStr) const
    {
        uint64_t hash = 0;
        for (int i = rStr.length() - 1; i >= 0; i--)
        {
            char character = rStr[rStr.length() - i - 1];
            hash += static_cast<uint8_t>(character) * (pow(256, i));
        }
        return hash % m_size;
    }

    /**
     * @brief Increases the size of the hash
     * map to the next prime number. Subsequently,
     * all key:value pairs will be rehashed
    */
    void Rehash()
    {
        // Resize to at least twice the current
        m_size = NextPrime(m_size * 2);

        String* pNewKeys = new String[m_size];
        T* pNewValues = new T[m_size];

        // For every element, rehash into the new arrays
        for (uint32_t i = 0; i < m_numElements; i++)
        {
            uint32_t hash = CalculateHash(m_pKeys[i]);
            if (pNewKeys[hash] == "")
            {
                pNewKeys[hash] = m_pKeys[i];
                pNewValues[hash] = m_pValues[i];
            }
            else
            {
                for (uint32_t i = hash + 1; i < hash; i = (i + 1) % m_size)
                {
                    if (pNewKeys[i] == "")
                    {
                        pNewKeys[hash] = m_pKeys[i];
                        pNewValues[hash] = m_pValues[i];
                    }
                }
            }
        }

        // Delete old arrays
        delete[] m_pKeys;
        delete[] m_pValues;

        // Update pointers to the new arrays
        m_pKeys = pNewKeys;
        m_pValues = pNewValues;
    }

    /**
     * @brief Helper method to determine the
     * next prime number after the given number
     *
     * @param[in] N    Starting point
     * @return The next prime number greater than n
    */
    int NextPrime(const int N) const
    {
        // Base case
        if (N <= 1) return 2;

        int prime = N;
        bool found = false;

        // Loop continuously until IsPrime returns
        // true for a number greater than n
        while (!found)
        {
            prime++;

            if (IsPrime(prime))
            {
                found = true;
            }
        }

        return prime;
    }

    /**
     * @brief Helper method to determine if a
     * number is prime or not
     *
     * @param[in] n    Number to investigate
     * @return Whether number is prime
     *      @retval true    - Number is prime
     *      @retval false   - Number is not prime
    */
    bool IsPrime(const int n) const
    {
        // Corner cases
        if (n <= 1)  return false;
        if (n <= 3)  return true;

        // This is checked so that we can skip
        // middle five numbers in below loop
        if (n % 2 == 0 || n % 3 == 0) return false;

        for (int i = 5; i * i <= n; i = i + 6)
        {
            if (n % i == 0 || n % (i + 2) == 0)
            {
                return false;
            }
        }
        return true;
    }
};

#endif // HASH_MAP_HPP
