/**
 * @file ServiceQueue.hpp
*/
#ifndef SERVICE_QUEUE_HPP
#define SERVICE_QUEUE_HPP

// SYSTEM INCLUDE
#include <queue>
#include <mutex>
#include <condition_variable>

// C++ PROJECT INCLUDE
// (None)

// FORWARD REFERENCES
// (None)

namespace Common
{

/**
 * @class ServiceQueue
 * 
 * @tparam Type to be stored in queue
*/
template <typename T>
class ServiceQueue
{
public:
    /**
     * Creates a new ServiceQueue object
    */
    ServiceQueue() :
        m_queue(),
        m_queueMutex(),
        m_queueCondVar()
    {}

    /**
     * @brief Pushes a new object onto the queue and notifies
     * any thread waiting on the conditional variable
     * 
     * @param item      Item to be added
    */
    void Push(T item)
    {
        // Lock the queue
        std::lock_guard<std::mutex> guard(m_queueMutex);
        
        // Push the item
        m_queue.push(item);

        // Notify thread that element has been added
        m_queueCondVar.notify_one();
    }

    /**
     * @brief Pops an element from the queue. If there are none,
     * it will wait on the queue's conditional variable
     * 
     * @warning This method has the potential to block
     * 
     * @return Element at the front of the queue
    */
    T Pop()
    {
        // Lock the queue
        std::unique_lock<std::mutex> lock(m_queueMutex);

        // Wait on the conditional variable while the queue's empty
        while (m_queue.size() == 0)
        {
            m_queueCondVar.wait(lock);
        }

        // Item was found, so pop it
        T item = m_queue.front();
        m_queue.pop();

        // We're done with the queue now
        lock.unlock();

        return item;
    }

    /**
     * @brief Retrieves the number of objects on the queue
     * 
     * @return Number of elements on the queue
    */
    uint32_t GetSize() const
    {
        // Lock the queue
        std::lock_guard<std::mutex> guard(m_queueMutex);

        // Return the size
        return m_queue.size();
    }

protected:
private:
    /// Actual queue to hold the objects
    std::queue<T> m_queue;

    /// Mutex to protect the queue
    std::mutex m_queueMutex;

    /// Condition variable to sleep and wakeup worker threads
    std::condition_variable m_queueCondVar;
};

} // namespace Common

#endif // SERVICE_QUEUE_HPP
