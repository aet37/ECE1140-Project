
/**
 * @file TrainModelData.hpp
*/
#ifndef TRAINMODELDATA_HPP
#define TRAINMODELDATA_HPP

// SYSTEM INCLUDES
// (none)

namespace TrainModel
{
int trainlength;
int speedLimit;
int power;
void setTrainLength(int len)
{
    trainlength = len;
}
int getTrainLength()
{
    return trainlength;
}
void setPower(int pow)
{
    power = pow;
}
int getPower()
{
    return power;
}

} // namespace TrainModel

#endif // TRAINMODELDATA_HPP
