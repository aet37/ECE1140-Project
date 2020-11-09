/**
 * @file Timekeeper.cpp
*/

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
#include "Timekeeper.hpp" // Header for class
#include "Assert.hpp" // For ASSERT
#include "ServiceQueue.hpp" // For ServiceQueue
#include "Request.hpp" // For Request

namespace Common
{

void Timekeeper::KeepTime()
{

}

void Timekeeper::AddPeriodicTimer(uint32_t periodInMs, ServiceQueue<Request>* pServiceQueue)
{
    ASSERT(pServiceQueue != nullptr);

    // Create a new timer
    Timer timer(periodInMs, pServiceQueue);

    // Lock the list in case the time keeper is running
    std::lock_guard<std::mutex> guard(m_listMutex);
    m_timerList.push_back(timer);
}

void Timekeeper::AddPointTimer(uint32_t time, ServiceQueue<Request>* pServiceQueue)
{
    // TODO(AET): Implement this method
}

Timekeeper::Timer::Timer(uint32_t periodInMs, ServiceQueue<Request>* pServiceQueue) :
    m_periodInMs(periodInMs),
    m_pServiceQueue(pServiceQueue)
{
    if (periodInMs == 0)
    {
        // TODO(AET): Fill this in for point timers
    }
    else
    {
        m_timeRemainingInMs = periodInMs;
    }
}

} // namespace Common
