/**
 * @file List.hpp
 * 
 * @brief Declarations and implementation for 
 * array backed list
*/
#ifndef ARRAY_LIST_HPP
#define ARRAY_LIST_HPP

// SYSTEM INCLUDES
#include <assert.h>

// C++ PROJECT INCLUDES
// (None)

/**
 * @class List
 * 
 * @brief Array-backed list class
 * @tparam T type stored in list
*/
template <typename T>
class List
{
public:
    /**
     * @brief Constructs a new List object
     * 
     * @param[in] initialSize Initial size of list
    */
    List(uint32_t initialSize = 10) :
        m_length(0),
        m_arraySize(initialSize),
        m_list(new T[initialSize])
    {}

    /**
     * @brief Destroys the List object
    */
    ~List()
    {
        delete[] m_list;
    }

    /// Delete copy constructor
    List(const List& rOther) = delete;

    /// Delete assignment operator
    List& operator=(List const&) = delete;

    /**
     * @brief Appends an element to the end of the list
     * 
     * @param element   Element to be inserted
    */
    void Append(T element)
    {
        // If the array is filled, resize it
        if (m_arraySize == m_length)
        {
            this->Resize();
        }

        m_list[m_length++] = element;
    }

    /**
     * @brief Operator[]
    */
    T& operator[](const uint32_t index)
    {
        assert(index < m_length);
        return m_list[index];
    }

    /**
     * @brief Operator[]
    */
    const T& operator[](const uint32_t index) const
    {
        assert(index < m_length);
        return m_list[index];
    }

    /**
     * @brief Clears the list
    */
    void Clear(void) { m_length = 0; }

    /**
     * @brief Gets the length member
    */
    uint32_t GetLength(void) const
    {
        return this->m_length;
    }

protected:

private:

    /// Number of elements in the list
    uint32_t m_length;

    /// Size of the array
    uint32_t m_arraySize;

    /// Array of elements
    T* m_list;

    /**
     * @brief Resizes the internal array
     * by a factor of two
    */
    void Resize()
    {
        m_arraySize *= 2;
        T* newList = new T[m_arraySize];
        for (uint32_t i = 0; i < m_length; i++)
        {
            newList[i] = m_list[i];
        }
        delete[] m_list;
        m_list = newList;
    }

};

#endif