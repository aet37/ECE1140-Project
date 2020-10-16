/**
 * @file Rung.hpp
 * 
 * @brief Declarations for the Rung class
*/
#ifndef RUNG_HPP
#define RUNG_HPP

// SYSTEM INCLUDES
// (None)

// C++ PROJECT INCLUDES
// (None)

/**
 * @class Rung
 * 
 * @brief Representation of a ladder logic rung
*/
class Rung
{
public:
    /**
     * @brief Constructs a new rung object
    */
    Rung() :
        m_pNextRung(nullptr)
    {}

    /**
     * @brief Executes the instructions on this rung
    */
    void Execute();
protected:
private:
    /// Pointer to the next rung to be executed
    Rung* m_pNextRung;
};

#endif // RUNG_HPP
