#ifndef LIST_HPP
#define LIST_HPP

#include <stdint.h>

template <typename T>

class List
{
    private:
    
    uint32_t m_length;

    uint32_t m_arraySize;

    T* m_list;

    void Resize()
    {
        m_arraySize *= 2;
        T* newList = new T[m_arraySize];
        for(uint32_t i=0; i<m_length; i++)
        {
            newList[i] = m_list[i];
        }
        delete[] m_list;
        m_list = newList;
    }

    public:

    List(uint32_t initialSize=10) :
    m_length(0),
    m_arraySize(initialSize),
    m_list(new T[initialSize])
    {}

    ~List()
    {
        delete[] m_list;
    }

    List(const List& rOther) = delete;

    List& operator = (List const&) = delete;

    void Append(T element)
    {
        if (m_arraySize == m_length)
        {
            Resize();
        }

        m_list[m_length++]=element;
    }

    T& operator[](const uint32_t index)
    {
        assert(index < m_length);
        return m_list [index];
    }

    const T& operator[](const uint32_t index) const
    {
        assert(index < m_length);
        return m_list[index];
    }

    void Insert(T element, uint32_t index)
    {
        assert (index <= m_length);

        if(m_arraySize == m_length)
        {
            Resize();
        }

        if(index == m_length)
        {
            Append(element);
            return;
        }

        for(int32_t i = m_length-1; i>=0; i--)
        {
            m_list[i+1] = m_list[i];
            if (i == index)
            {
                m_list[i] = element;
                m_length++;
                break;
            }
        }
    }

    T Remove(uint32_t index)
    {
        assert(index <= (m_length-1));

        T oldValue = m_lise [index];

        for (uint32_t i =index; i < m_length - 1; i++)
        {
            m_list[i] = m_list[i+1];
        }
        m_length--;
        return oldValue;
    }

    void Clear() 
    {
        m_length=0;
    }

    uint32_t getLength() const
    {
        return m_length;
    }

    bool IsEmpty() const
    {
        return m_length==0;
    }

};

#endif