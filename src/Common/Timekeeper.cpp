/**
 * @file Timekeeper.cpp
*/

// SYSTEM INCLUDES
#include <chrono>
#include <thread>

// C++ PROJECT INCLUDES
#include "Timekeeper.hpp" // Header for class
#include "Assert.hpp" // For ASSERT
#include "ServiceQueue.hpp" // For ServiceQueue
#include "Request.hpp" // For Request

namespace Common
{

void Timekeeper::KeepTime()
{
    while (true)
    {
        // Sleep until the next timer should expire
        std::this_thread::sleep_for(std::chrono::milliseconds(m_sleepDurationInMs));

        // Reset the sleep duration to max sleep
        m_sleepDurationInMs = MAX_SLEEP_DURATION_IN_MS;

        // Iterate through the timer list
        for (int i = 0; i < m_timerList.size(); i++)
        {
            // Subtract the elapsed time from each timer's time remaining
            Timer& rTimer = m_timerList[i];
            rTimer.m_timeRemainingInMs -= m_sleepDurationInMs;

            // Emit the event if there is no time remaining
            if (rTimer.m_timeRemainingInMs == 0)
            {
                rTimer.m_pServiceQueue->Push(Request(RequestCode::TIMER_EXPIRED));

                // Reset the timer using its period
                rTimer.m_timeRemainingInMs = rTimer.m_periodInMs;
            }

            // Keep track of how long we should sleep for by finding the lowest time remaining
            if (rTimer.m_timeRemainingInMs < m_sleepDurationInMs)
            {
                m_sleepDurationInMs = rTimer.m_timeRemainingInMs;
            }
        }
    }
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
