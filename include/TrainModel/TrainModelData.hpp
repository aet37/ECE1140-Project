
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
void setTrainLength(int len)
{
    trainlength = len;
}
int getTrainLength()
{
    return trainlength;
}

} // namespace TrainModel

#endif // TRAINMODELDATA_HPP