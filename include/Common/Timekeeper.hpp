/**
 * @file Timekeeper.hpp
*/
#ifndef TIMEKEEPER_HPP
#define TIMEKEEPER_HPP

// SYSTEM INCLUDES
#include <vector>
#include <mutex>

// C++ PROJECT INCLUDES
// (None)

namespace Common
{

// FORWARD DECLARATIONS
template <typename T>
class ServiceQueue;
class Request;

class Timekeeper
{
public:
    /// Period used for the power - velocity loop
    static const uint32_t SAMPLING_PERIOD_IN_MS = 1000;
    
    /**
     * @brief Gets the singleton instance
    */
    static Timekeeper& GetInstance()
    {
        static Timekeeper* pInstance = new Timekeeper();
        return *(pInstance);
    }

    /**
     * @brief Thread function to keep time of the simulation
    */
    void KeepTime();

    /**
     * @brief Requests this class to place the TIMER_EXPIRED event on the given queue
     * at the given period
     *
     * @param periodInMs        Period of the timer
     * @param pServiceQueue     Queue on which to push an event
    */
    void AddPeriodicTimer(uint32_t periodInMs, ServiceQueue<Request>* pServiceQueue);

    /**
     * @brief Requests this class to place a TIMER_EXPIRED event on the given queue
     * at the given time. Simulation starts at time = 0
     *
     * @param time              Time at which the timer should expire
     * @param pServiceQueue     Queue on which to push an event
    */
    void AddPointTimer(uint32_t time, ServiceQueue<Request>* pServiceQueue);
protected:
private:
    /// Max amount of time the thread can sleep for
    static const uint32_t MAX_SLEEP_DURATION_IN_MS = 5000;

    /**
     * @struct Timer
    */
    typedef struct Timer
    {
        /// Period of the timer, zero if it's a point timer
        uint32_t m_periodInMs;

        /// Timer remaining since starting this timer
        int32_t m_timeRemainingInMs;

        /// Service queue that the event will go onto
        ServiceQueue<Request>* m_pServiceQueue;

        /**
         * @brief Constructs a new Timer object
        */
        Timer(uint32_t periodInMs, ServiceQueue<Request>* serviceQueue);
    } Timer;

    /// List of timers
    std::vector<Timer> m_timerList;

    /// Mutex for the list
    std::mutex m_listMutex;

    /// Amount of time until the next timer should expire
    uint32_t m_sleepDurationInMs;

    /**
     * @brief Constructs a new Timekeeper object
     *
     * @note Private to ensure singleton
    */
    Timekeeper() :
        m_timerList(),
        m_listMutex(),
        m_sleepDurationInMs(MAX_SLEEP_DURATION_IN_MS)
    {}
};

} // namespace Common

#endif // TIMEKEEPER_HPP
