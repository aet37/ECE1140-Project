/**
 * @file ServiceQueueUT.cpp
*/

// SYSTEM INCLUDES
#include <chrono>
#include <thread>
#include <iostream>

// C++ PROJECT INCLUDES
#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators_all.hpp>
#include "ServiceQueue.hpp" // UUT

static int testVariable = 0;
static Common::ServiceQueue<int> serviceQueue;
static bool testActive = true;

void consumerThreadFunction()
{
    while (testActive)
    {
        // Expected to block here
        int temp = serviceQueue.Pop();
        testVariable = temp;
    }
}

/**
 * PRECONDITIONS: Thread is started, queue is empty
 * EXECUTION: Producer pushes integers onto the queue. A maximum of 1 second is
 * waited for the consumer to pick up the integer
 * POSTCONDITIONS: Shared variable has been set by consuming thread
*/
TEST_CASE("Simple Producer-Consumer")
{
    std::thread consumer(consumerThreadFunction);

    for (int producedData = 1; producedData < 13; producedData += 2)
    {
        REQUIRE(producedData != testVariable);

        serviceQueue.Push(producedData);

        auto start = std::chrono::steady_clock::now();
        const std::chrono::duration<double> TIMEOUT = std::chrono::seconds(1);
        while (testVariable != producedData)
        {
            std::chrono::duration<double> elapsedTime = std::chrono::steady_clock::now() - start;
            if (elapsedTime > TIMEOUT)
            {
                FAIL();
            }
        }

        REQUIRE(producedData == testVariable);
    }

    testActive = false;
    serviceQueue.Push(1);

    SUCCEED();

    consumer.join();
}
