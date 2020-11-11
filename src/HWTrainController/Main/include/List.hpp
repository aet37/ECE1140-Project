/**
 * @file List.hpp
 *
 * @brief Declarations and implementation for
 * array backed list
*/
#ifndef LIST_HPP
#define LIST_HPP

// SYSTEM INCLUDES
#include <assert.h>
#include <stdint.h>

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
    explicit List(uint32_t initialSize = 10) :
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
            Resize();
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
     * @brief Inserts the given element at the given position
    */
    void Insert(T element, uint32_t index)
    {
        assert(index <= m_length);
        // If the array is filled, resize it
        if (m_arraySize == m_length)
        {
            Resize();
        }

        // If we are just appending, use that method
        if (index == m_length)
        {
            Append(element);
            return;
        }

        for (int32_t i = m_length - 1; i >= 0; i--)
        {
            m_list[i + 1] = m_list[i];
            if (i == index)
            {
                m_list[i] = element;
                m_length++;
                break;
            }
        }
    }

    /**
     * @brief Removes the element at the given index
     *
     * @param index     Index of element to remove
     * @return Element that was removed
    */
    T Remove(uint32_t index)
    {
        // Bounds check
        assert(index <= (m_length - 1));

        T oldValue = m_list[index];

        for (uint32_t i = index; i < m_length - 1; i++)
        {
            m_list[i] = m_list[i+1];
        }
        m_length--;
        return oldValue;
    }

    /**
     * @brief Clears the list
    */
    void Clear(void) { m_length = 0; }

    /**
     * @brief Gets the length member
    */
    uint32_t GetLength() const
    {
        return m_length;
    }

    /**
     * @brief Whether the list is empty
    */
    bool IsEmpty() const
    {
        return m_length == 0;
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

#endif // LIST_HPP
